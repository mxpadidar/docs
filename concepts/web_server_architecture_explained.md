# Understanding Your Web Stack: Load Balancers, Web Servers, and Application Servers

## 1. The Core Problem: Where Did My User's IP Address Go?

When building a web application, a frequent and critical challenge is correctly identifying the IP address of the end-user. This is essential for logging, security (like rate limiting), and location-based services.

The confusion arises because as an application's architecture grows, the user's request is passed through multiple layers. Each "hop" in this chain can obscure the original source IP address.

This document explains the role of each component in a modern web stack and clarifies how network connections are handled at each step, so you can reliably find the user's real IP.

---

## 2. The Players: A Three-Tier Analogy

Think of a busy restaurant. You don't just walk into the kitchen to get your food. There's a process.

1.  **The Load Balancer (The Host/Maître d'):** The first point of contact. They greet guests, manage the queue, and decide which waiter can handle a new table. They don't take the order themselves, but they manage the flow.
2.  **The Web Server (The Waiter):** The waiter takes your order. They are excellent at handling many concurrent requests efficiently (taking orders, delivering food, bringing drinks). They might handle simple requests themselves (like bringing water) or pass complex food orders to the kitchen.
3.  **The Application Server (The Kitchen):** The kitchen is where the actual "work" happens. It takes the order from the waiter and prepares the complex meal (i.e., runs your application logic, queries the database). It's highly specialized but not great at talking directly to hundreds of customers at once.

In our stack:

- **Load Balancer:** Nginx, HAProxy, AWS ELB, Cloudflare
- **Web Server:** Nginx, Apache
- **Application Server:** Gunicorn, Uvicorn (for Python), Puma (for Ruby), Tomcat (for Java)

---

## 3. Network Layers: A Quick Primer (The TCP/IP Model)

To understand how these components talk, we only need to focus on three layers of the network.

- **Layer 3: Network Layer (IP)**
  - **Job:** Global Addressing.
  - **Analogy:** The full mailing address on an envelope (e.g., `8.8.8.8`). Every device on the internet has one.

- **Layer 4: Transport Layer (TCP)**
  - **Job:** Creating a reliable, direct connection between two devices.
  - **Analogy:** Making a direct phone call. A connection is established between a **source IP/port** and a **destination IP/port**. **This is the most critical concept.**

- **Layer 7: Application Layer (HTTP)**
  - **Job:** Defining the language of the application.
  - **Analogy:** The actual conversation you have over the phone (`GET /home`, `POST /login`). Devices that can understand this language are "Layer 7" devices.

**Key Rule:** A TCP connection (Layer 4) can only exist between two points. If a third device is introduced in the middle (like a proxy), it _must_ create a second, separate connection.

---

## 4. Scenario 1: The Simple Setup (No Load Balancer)

For most applications, you don't need a dedicated load balancer. You just have a single server running your stack. However, even here, there are two distinct "hops."

**Architecture:**
`User -> Nginx (Web Server) -> Gunicorn/Uvicorn (App Server)`

```
                  THE INTERNET
                      |
                      | 1. Connection #1 from User IP: 8.8.8.8
                      |
+---------------------V---------------------+
| YOUR SERVER                               |
|                                           |
|   +-----------------------------------+   |
|   |          NGINX (Web Server)       |   |
|   |-----------------------------------|   |
|   | Sees real IP: `8.8.8.8`           |   |
|   | Sets header: `X-F-F: 8.8.8.8`     |   |
|   +-----------------------------------+   |
|                      |                    |
|                      | 2. Connection #2 (from localhost)
|                      |                    |
|   +------------------V----------------+   |
|   |    GUNICORN / Uvicorn (App Server)  |   |
|   |-----------------------------------|   |
|   | Sees IP: `127.0.0.1`              |   |
|   | Reads `X-Forwarded-For` header    |   |
|   +-----------------------------------+   |
+-------------------------------------------+
```

### The Flow:

1.  **Connection #1 (User to Nginx):**
    - The user at `8.8.8.8` establishes a TCP connection directly with your server's public IP.
    - **Nginx is at the edge.** It receives this connection. From its perspective, the source IP of this connection (`$remote_addr`) is `8.8.8.8`. **It sees the real IP.**

2.  **The "Handoff" (Nginx as a Reverse Proxy):**
    - Nginx is a Layer 7 device. It reads the HTTP request. Its job is to pass this request to the Application Server (Gunicorn), which is waiting for internal connections.
    - To do this, Nginx creates **Connection #2**.

3.  **Connection #2 (Nginx to Gunicorn):**
    - Nginx establishes a _new_ TCP connection to the Application Server, which is usually listening on `127.0.0.1:8000` (localhost).
    - From Gunicorn's perspective, the source IP of this connection is `127.0.0.1`. **It does not see the real user IP.**

4.  **Passing the Information:**
    - Because Nginx is a smart Layer 7 proxy, it knows the original IP is lost. So, before it sends the request over Connection #2, it adds a header:
      `X-Forwarded-For: 8.8.8.8`
    - Your application framework (e.g., FastAPI, Django) must be configured to look for and trust this header to get the real user IP.

### Example Nginx Configuration (`nginx.conf`):

```nginx
server {
    listen 80;
    server_name yourdomain.com;

    location / {
        # Pass the request to your application server
        proxy_pass http://127.0.0.1:8000;

        # Set headers so the app server knows the real details
        proxy_set_header Host $host;
        # Set the user's real IP address from the incoming connection
        proxy_set_header X-Forwarded-For $remote_addr;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

---

## 5. Scenario 2: The Scalable Setup (With a Load Balancer)

When your application needs to handle high traffic or be highly available, you introduce a Load Balancer.

**Architecture:**
`User -> Load Balancer -> Nginx (Web Server) -> Gunicorn (App Server)`

The principle is **exactly the same**, just with one more link in the chain.

```
User IP: 8.8.8.8
       |
       | Connection #1
       V
Load Balancer (e.g., AWS ELB)
   - Sees Real IP: `8.8.8.8`
   - Adds Header: `X-Forwarded-For: 8.8.8.8`
       |
       | Connection #2
       V
Nginx Web Server
   - Sees IP of Load Balancer (e.g., `10.0.1.50`)
   - Reads `X-F-F: 8.8.8.8`
   - Appends its own IP to the header: `X-F-F: 8.8.8.8, 10.0.1.50`
       |
       | Connection #3
       V
Gunicorn Application Server
   - Sees IP of Nginx Web Server (`127.0.0.1`)
   - Reads `X-Forwarded-For` header. The first IP in the list is the user's.
```

### The Security Risk: Spoofing `X-Forwarded-For`

- **The Problem:** What if an attacker sends a request directly to your Nginx Web Server with a fake header: `X-Forwarded-For: 1.2.3.4`? If your application blindly trusts this header, it will think the attacker is `1.2.3.4`.
- **The Solution:** Your server must be configured to **only trust the `X-Forwarded-For` header when the connection comes from a trusted IP address.**
  - In Scenario 1, your application server should only trust this header for requests from `127.0.0.1` (Nginx).
  - In Scenario 2, your Nginx server should only trust this header for requests from the Load Balancer's IP address. This is done in Nginx with the `set_real_ip_from` directive.

## Conclusion

The rule is simple: **Only the component at the very edge of the network sees the true source IP from the network layer.**

Every subsequent component in the chain will only see the IP of the component that came immediately before it. Therefore, it is the responsibility of each "hop" to read the real IP and pass it along in an HTTP header (`X-Forwarded-For`) for the next hop to consume.

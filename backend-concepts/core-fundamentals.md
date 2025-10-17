# Core Backend Concepts

## What Happens When You Type a URL and Press Enter?

When you type a **Uniform Resource Locator (URL)** into your browser and press Enter, a complex sequence of networking and application-layer protocols initiates a process to fetch and display the requested content. This process bridges the gap between the human-readable domain name and the numerical address computers use.

### 1. DNS Resolution (Finding the Server)

The browser's first task is to translate the **domain name** into an **IP address**. This is done using the **Domain Name System (DNS)**, often called the "phonebook of the internet."

1.  **Cache Check:** The browser first checks its own cache, the Operating System (OS) cache, the router cache, and the ISP's DNS cache for the IP address.
2.  **DNS Query:** If the address isn't cached, a request is sent to a **recursive DNS resolver** (usually managed by your ISP).
3.  **Recursive Search:** The resolver performs a recursive search:
    - It asks the **Root Name Server** where to find the **TLD (Top-Level Domain) Name Server** (e.g., the `.com` server).
    - It asks the TLD server where to find the **Authoritative Name Server** for the specific domain (`example.com`).
    - The Authoritative Name Server returns the correct **IP address** to the resolver, which then passes it back to the browser.

### 2. TCP Handshake and TLS Negotiation

Once the IP address is known, the browser must establish a reliable connection to the server.

- **TCP Handshake (SYN/ACK):** The browser initiates a **Transmission Control Protocol (TCP)** connection by performing a **three-way handshake** (SYN, SYN-ACK, ACK) to ensure both client and server are ready to communicate.
- **TLS/SSL Handshake (for HTTPS):** If the URL uses **HTTPS** (which it almost always does today), a **Transport Layer Security (TLS)** handshake follows the TCP handshake. This process securely exchanges encryption keys, allowing all subsequent data transfer to be encrypted, protecting data privacy and integrity.

### 3. HTTP Request Sent to Server

With a secure connection established, the browser constructs and sends an **HTTP Request** to the server at its IP address.

- **Request Components:** The request includes:
  - **Method:** (e.g., `GET` to retrieve data, `POST` to send data).
  - **Path:** The specific resource being requested (e.g., `/index.html` or `/users`).
  - **Headers:** Metadata about the request (e.g., `Host`, `User-Agent`, `Accept-Language`, and any relevant **Cookies**).

### 4. Server Processing and Response

The web server receives the request, processes it, and formulates a response.

1.  **Request Processing:** The server software (e.g., Apache, Nginx) passes the request to the application code (e.g., written in Python, Node.js, Java) which interacts with databases, runs logic, and generates the final content.
2.  **HTTP Response:** The server constructs an **HTTP Response** which contains:
    - **Status Line:** Includes the **HTTP Status Code** (e.g., `200 OK` for success, `404 Not Found`, `500 Internal Server Error`).
    - **Headers:** Metadata about the response (e.g., `Content-Type`, `Set-Cookie`).
    - **Body:** The requested data, typically HTML, CSS, JSON, or an image file.

### 5. Browser Rendering

The browser receives the response and begins rendering the webpage for the user.

1.  **Parsing:** The browser reads the **HTML** and constructs the **Document Object Model (DOM)**.
2.  **Resource Fetching:** As it parses the HTML, it discovers links to other resources (CSS, JavaScript, images) and immediately initiates **new HTTP requests** to fetch them.
3.  **Styling and Layout:** The **CSS** is loaded, parsed, and used to calculate the visual styles and layout of the page elements.
4.  **JavaScript Execution:** **JavaScript** is loaded and executed, which can modify the DOM and add interactivity to the page.
5.  **Display:** The browser progressively displays the fully rendered page to the user.

---

## **Web Servers vs. Application Servers**

Modern backend architectures separate **network-level request handling** (web servers) from **application-level execution** (application servers).
This separation improves scalability, security, and maintainability.

### Web Server (Frontline Request Receiver)

A **Web Server** (like **Nginx** or **Apache**) is responsible for:

- Accepting and managing **incoming HTTP/TCP connections** from clients.
- Performing **TLS termination** (decrypting HTTPS).
- Serving **static assets** (e.g., images, CSS, JS) directly.
- Acting as a **Reverse Proxy**, forwarding dynamic requests to an **Application Server**.
- Handling **load balancing**, **caching**, and **rate limiting**.

_Think of the Web Server as the “traffic cop” directing requests to where the real logic lives._

### Application Server (Code Executor)

An **Application Server** runs your actual **backend code** (e.g., Django, FastAPI, Flask, Spring, Node.js).
It doesn’t handle direct network traffic at scale — instead, it listens on local sockets or ports for requests forwarded by the web server.

**Responsibilities:**

- Parse incoming HTTP requests (headers, body, method, etc.).
- Invoke the web framework (e.g., Django, Flask, FastAPI).
- Manage **workers/processes/threads** to handle multiple concurrent requests.
- Execute **application logic**, **database queries**, and **serialization**.
- Build and return HTTP responses to the Web Server.

### Common Python Application Servers

**Gunicorn** — A WSGI-compatible server used by frameworks like Django and Flask. It’s a multi-process, battle-tested server designed for synchronous web applications and is one of the most stable production choices for Python web apps.

**Uvicorn** — An ASGI server built for asynchronous frameworks such as FastAPI, Starlette, and modern async-enabled Django. It’s lightweight, extremely fast, and ideal for high-throughput, non-blocking applications.

**Waitress** — A pure-Python WSGI server often used with frameworks like Pyramid or Flask. It’s simple to configure, reliable, and works well on Windows environments or smaller deployments.

**Daphne** — Django Channels’ reference ASGI server, built to support long-lived connections and real-time communication like WebSockets. Suitable when your Django app needs asynchronous features.

### Why Separate the Web Server and Application Server?

- **Security:** The web server (e.g., Nginx) acts as a reverse proxy, isolating the application server from direct public access.
- **Performance:** It handles static files and persistent connections (keep-alive, SSL termination) more efficiently than Python processes.
- **Scalability:** You can run multiple application servers behind one web server, load balancing traffic between them.
- **Flexibility:** The network architecture remains stable — you can switch frameworks or app servers without touching the proxy setup.

### Django Development vs. Production

In **development**, Django uses a lightweight built-in **WSGI/ASGI server** (based on `wsgiref`) when you run
`python manage.py runserver`. This server is designed for debugging and local testing only.
In **production**, always deploy Django behind a dedicated **Application Server** (like **Gunicorn** or **Uvicorn**)
and a **Web Server** (such as **Nginx** or **Apache**) for performance, scalability, and security.

---

## **Difference between reverse proxy and forward proxy**

- **Forward Proxy**: Acts on behalf of clients to access external servers. Often used for anonymity, caching, or access control. The server sees requests coming from the proxy, not the client.

- **Reverse Proxy**: Acts on behalf of servers to handle client requests. Provides load balancing, SSL termination, caching, and security. Clients do not know the actual backend servers.

## **Server-Side Request Handling Lifecycle**

When an HTTP request successfully reaches a backend server, it goes through a defined, multi-stage process from the network interface to the application code, culminating in a response being sent back to the client.

### 1. Web Server Acceptance and Hand-off

- The request is received by a **Load Balancer** or **Web Server** (e.g., Nginx, Apache).
- If using HTTPS, **TLS Termination** (decrypting the request) occurs here.
- The Web Server acts as a **Reverse Proxy**, forwarding the processed HTTP request over a local interface (like a socket) to the actual **Application Server** (e.g., **Gunicorn**, **Uvicorn**, Tomcat, or a Node.js process).

### 2. Request Parsing and Middleware

- The **Application Framework** (e.g., Express, Django, Spring) running on the Application Server receives the raw request.
- The framework parses the request body, headers, query parameters, and URL path.
- **Middleware** functions execute global logic, such as:
  - Logging the request details.
  - Checking for a valid **Authentication** token (e.g., JWT).
  - Performing basic data validation.

### 3. Routing and Controller Selection

- The **Router** component matches the incoming URL path and HTTP method (e.g., `GET /users/10`) to a specific **Route Handler** or **Controller** function defined in the application code.
- This determines the entry point for the required **Business Logic**.

### 4. Business Logic and Service Execution

- The **Controller** executes the core **Business Logic**, often involving a **Service Layer**.
- This layer contains the main application logic, performing calculations, making decisions, and managing complex workflows.

### 5. Data Layer Interaction (Database)

- If the request requires persistent data, the Service Layer uses a **Data Access Layer (DAL)** or **ORM** (Object-Relational Mapper) to communicate with the **Database** (e.g., PostgreSQL, MongoDB).
- Data is fetched, modified, or stored as required by the business logic.

### 6. Response Construction and Serialization

- The application gathers the final result (e.g., a list of users, a confirmation message).
- The result is formatted into the required output structure, typically **JSON** or **XML** for APIs, or rendered as **HTML** for traditional web pages.
- The correct **HTTP Status Code** (e.g., `200 OK`, `201 Created`, `400 Bad Request`) and necessary **Headers** (e.g., `Content-Type`) are attached.

### 7. Response Transmission

- The complete HTTP response is sent back through the Application Server to the initial **Web Server/Load Balancer**.
- If TLS was terminated earlier, the response is **re-encrypted** here.
- The Web Server sends the encrypted response over the network back to the client's browser.

---

## **Load Balancing (Scaling Traffic)**

**Load Balancing** is the process of distributing incoming network traffic across multiple backend servers to ensure no single server is overwhelmed. This maximizes throughput, minimizes latency, and provides high availability.

### Core Functions

- **Traffic Distribution:** Spreads client requests across a pool of servers to optimize resource usage.
- **High Availability:** Automatically detects server failures (via **Health Checks**) and redirects traffic to the remaining healthy servers, preventing downtime.
- **Horizontal Scaling:** Allows developers to easily add or remove servers to handle fluctuating traffic loads.

### Load Balancer Types

Load balancers operate at different levels to inspect the traffic:

- **Layer 4 (Transport Layer):** Distributes traffic based only on **IP address** and **port**. It's fast and focuses on simple, high-speed forwarding (TCP/UDP).
- **Layer 7 (Application Layer):** Distributes traffic based on the content of the HTTP request, such as the **URL path** or **headers**. This enables features like **SSL termination** and content-based routing.

### Common Algorithms

Algorithms determine which server receives the next request:

- **Round Robin:** Distributes requests to servers sequentially, assuming they all have equal capacity.
- **Least Connection:** Sends the request to the server that currently has the lowest number of active client connections, making it ideal for varying load times.
- **Weighted Round Robin:** Assigns a "weight" to each server based on its capacity, ensuring more powerful servers receive a larger share of the traffic.

### Session Persistence

- **Concept:** Also called **Session Stickiness**, this ensures all requests from a single client are consistently routed to the _same_ backend server.
- **Need:** Required when the application stores user session data (state) directly on the specific backend server rather than a centralized location. Modern architectures try to avoid this by making servers **stateless**.

---

## **CORS (Cross-Origin Resource Sharing)**

**CORS** is a browser-enforced security mechanism that controls how a web page from one origin (domain, protocol, or port) can interact with resources from another origin. It exists to protect users from **malicious cross-origin requests** that could steal data or perform unauthorized actions. Enables controlled **cross-domain communication** between a browser-based frontend and an API hosted on a different origin. Without CORS, browsers enforce the **Same-Origin Policy**, blocking such requests for security.

- **Key Concepts:**
  - **Origin:** Defined by the combination of `scheme + host + port`.
    Example: `https://app.example.com` and `https://api.example.com` are **different origins**.

  - **Same-Origin Policy (SOP):** The browser blocks requests between different origins unless the target server explicitly allows them via CORS headers.

- **CORS Workflow:**
  1. The browser detects a cross-origin request (e.g., via `fetch` or `XHR`).
  2. It sends a **preflight request** (`OPTIONS` method) to check if the target server allows the operation.
  3. The server responds with specific headers granting or denying permission.

- **Important CORS Headers:**
  - **`Access-Control-Allow-Origin`:** Specifies which origins can access the resource (`*` for public APIs or a specific domain for controlled access).
  - **`Access-Control-Allow-Methods`:** Lists allowed HTTP methods (e.g., `GET, POST, PUT`).
  - **`Access-Control-Allow-Headers`:** Defines which custom headers (e.g., `Authorization`, `Content-Type`) are permitted in the request.
  - **`Access-Control-Allow-Credentials`:** Enables cookies or authentication headers to be sent with cross-origin requests.

- **Security Implications:**
  - CORS **does not make your API secure by itself** — it only defines who _can_ access it.
  - Incorrectly setting `Access-Control-Allow-Origin: *` with `Allow-Credentials: true` can expose sensitive data.
  - Always **limit allowed origins** in production to trusted domains.

- **Backend Implementation (Example):**

  ```python
  # Django Example
  CORS_ALLOWED_ORIGINS = ['https://frontend.example.com']

  # FastAPI Example
  from fastapi.middleware.cors import CORSMiddleware
  app.add_middleware(
      CORSMiddleware,
      allow_origins=["https://frontend.example.com"],
      allow_methods=["*"],
      allow_headers=["*"],
  )
  ```

---

## **What is Caching?**

**Caching** is the process of storing copies of frequently accessed data or computational results in a temporary, high-speed storage layer (the **cache**) so that future requests for that data can be served faster than fetching it from the primary source (like a database or an external API). The goal is to reduce latency and load on backend services.

### Key Caching Metrics

- **Cache Hit:** Occurs when the requested data is found in the cache.
- **Cache Miss:** Occurs when the requested data is not found in the cache, requiring the system to retrieve it from the slower, primary data source.
- **Time-To-Live (TTL):** The duration for which data is considered valid in the cache before it is marked as stale and needs to be refreshed.

## Application of Caching in Backend Systems

Caching can be applied at various points (layers) within a backend architecture to maximize performance.

### 1. Browser/Client-Side Caching

- **What is Cached:** Static assets like **HTML**, **CSS**, **JavaScript**, and images.
- **Mechanism:** Controlled by HTTP response headers (e.g., `Cache-Control`, `Expires`) which tell the browser how long to store the resource locally.

### 2. CDN Caching (Content Delivery Network)

- **What is Cached:** Copies of static assets and, sometimes, dynamically generated responses.
- **Mechanism:** CDNs distribute content to geographically dispersed servers (**edge locations**). This speeds up delivery by serving assets from the location closest to the user.

### 3. Application Cache (In-Memory)

- **What is Cached:** Results of expensive computations, configuration settings, or frequently accessed business objects.
- **Mechanism:** Data is stored directly in the application server's memory (e.g., using a built-in library or language features). This is the fastest form of caching but is volatile (data is lost on server restart) and doesn't scale easily across multiple server instances.

### 4. Distributed Cache (External Store)

- **What is Cached:** Session data, database query results, and API responses.
- **Mechanism:** Utilizes dedicated, highly optimized key-value stores like **Redis** or **Memcached**. This is the most common approach for scalable backend systems as it is non-volatile and shared by all application servers (**shared state**).

### 5. Database Caching

- **What is Cached:** The results of complex or common database queries.
- **Mechanism:** The database system (e.g., PostgreSQL, MySQL) maintains an internal buffer of frequently used data blocks or query results, reducing the need to read from disk.

### 6. Reverse Proxy Cache

- **What is Cached:** The full response from the backend application (e.g., a static JSON API response).
- **Mechanism:** A reverse proxy like **Nginx** or a specialized cache layer like **Varnish** sits in front of the application server and serves cached responses directly, preventing traffic from ever reaching the application code.

---

## **What’s the difference between HTTP and HTTPS?**

HTTP is an unsecured protocol for transferring data between client and server. HTTPS is HTTP layered over TLS, which encrypts the communication channel, ensuring data confidentiality, integrity, and authentication. HTTPS prevents interception and tampering by third parties.

---

## **What is REST? What is a RESTful API?**

REST (Representational State Transfer) is an architectural style for designing networked applications. It uses stateless communication and standard HTTP methods (GET, POST, PUT, DELETE) to manipulate resources identified by URLs. A RESTful API follows these principles, exposing resources as endpoints and exchanging data typically in JSON or XML format.

---

## **What is statelessness in REST?**

Statelessness means each request from a client to a server must contain all the information needed to understand and process it. The server does not store any session or client state between requests. This simplifies scaling and improves reliability, as any server instance can handle any request independently.

---

## **What are HTTP headers?**

HTTP headers are key-value pairs sent in requests and responses to convey metadata. They define how content is handled, authenticated, cached, and transmitted. Request headers describe client details or preferences; response headers provide information about the returned content or server behavior.

---

## **What are idempotent methods?**

Idempotent HTTP methods are those that can be called multiple times without changing the result beyond the initial application. For example, GET, PUT, and DELETE are idempotent because repeating the same request produces the same effect on the server. POST is not idempotent because each call can create new resources or trigger new actions.

---

## **HTTP status codes (less common but important)**

- **202 Accepted** — The request has been accepted for processing but not yet completed. Often used for async or queued operations.
- **301 Moved Permanently** — Resource permanently moved to a new URL. Used for redirects.
- **304 Not Modified** — Indicates the resource hasn’t changed; used with caching and conditional requests.
- **405 Method Not Allowed** — HTTP method not supported for the target resource.
- **409 Conflict** — Request conflicts with the current state of the resource (e.g., version mismatch).
- **410 Gone** — Resource is permanently removed and not expected to return.
- **415 Unsupported Media Type** — The server does not support the request’s content type.
- **422 Unprocessable Entity** — Request is well-formed but contains semantic errors (common in validation).
- **429 Too Many Requests** — Rate limit exceeded.
- **502 Bad Gateway** — Server acting as a gateway received an invalid response.
- **503 Service Unavailable** — Server is overloaded or down for maintenance.
- **504 Gateway Timeout** — Gateway or proxy did not receive a timely response.

## **Authentication and Authorization Essentials**

**Authentication** is the process of verifying a user's identity ("Who are you?"). **Authorization** is the process of verifying what an authenticated user is allowed to do ("What can you access?"). Good backend design always separates these two concerns.

### Key Authentication Methods

Different methods are used to verify identity, each with its own trade-offs regarding security, scalability, and complexity.

#### 1. Basic Authentication

- **Mechanism:** The client sends credentials (username and password) encoded in **Base64** within the `Authorization` header on _every_ request.
- **Security Note:** Basic Auth is not encrypted, only encoded. It **must** be used over **HTTPS** to prevent the credentials from being intercepted in plain text.
- **Use Case:** Often used for API access with simple clients or for server-to-server communication, not ideal for web browsers.

#### 2. Session-Based Authentication

- **Mechanism:** After successful login, the server creates a **Session Record** and sends a unique **Session ID** back to the client, usually stored in a secure, **`HttpOnly` cookie**.
- **Server State:** This method is **stateful**; the server must store and maintain the active session state, which can complicate scaling horizontally (adding more servers).
- **Security:** Strong security is achieved via the `HttpOnly` and `Secure` cookie attributes.

#### 3. Token-Based Authentication (JWT)

- **Mechanism:** After login, the server issues a **JWT** containing user claims (metadata). The client stores this token (often in memory) and sends it in the `Authorization` header as a **Bearer Token**.
- **Server State:** This method is primarily **stateless**; the server only validates the token's cryptographic signature and expiration, simplifying scaling.
- **Security:** Security relies on using a strong secret key for signing and ensuring short expiration times. Revocation is a common challenge.

#### 4. OAuth 2.0 (Delegated Authorization)

- **Mechanism:** A framework, not an authentication protocol itself, used to grant an application (the Client) **limited access** to a user's resources hosted by another service (the Resource Server), without giving the client the user's password.
- **Key Actors:** **Resource Owner** (the user), **Client** (the application seeking access), **Authorization Server** (handles the login and token issuance), and **Resource Server** (holds the data).
- **Use Case:** "Log in with Google/Facebook/etc." flows. It is primarily for **Authorization**, but often includes an **OpenID Connect (OIDC)** layer on top to handle the actual Authentication.

### Important Security Considerations

- **Principle of Least Privilege:** Users should only be authorized to access the resources absolutely necessary to perform their duties.
- **Hashing Passwords:** Never store passwords in plain text. Use slow, modern, salted hashing algorithms like **Bcrypt** or **Argon2** to securely store user credentials.
- **Rate Limiting:** Implement limits on the number of login attempts (and other requests) to prevent **brute-force attacks**.
- **Token/Session Expiration:** Always set a strict expiration time for tokens and sessions to limit the window of opportunity for an attacker if credentials are stolen.

---

## **Difference between Cookies, Sessions, and Tokens**

### Cookies

Cookies are small pieces of data stored by the browser on the client machine, automatically included in the headers of every request sent back to the originating server.

- **Core Function:** Used primarily for session management, personalization, and tracking.
- **Security Attributes (Key Extensions):**
  - **`HttpOnly`:** A flag set by the server that prevents client-side JavaScript from accessing the cookie. This is critical for mitigating **Cross-Site Scripting (XSS)** attacks, especially for cookies holding sensitive data like Session IDs or tokens.
  - **`Secure`:** A flag that instructs the browser to send the cookie **only** over encrypted HTTPS connections, preventing interception during transmission (**Man-in-the-Middle attacks**).
  - **`SameSite`:** Controls whether the cookie is sent with cross-site requests, which is essential for mitigating **Cross-Site Request Forgery (CSRF)** attacks. Recommended values are `Lax` or `Strict`.

### Sessions

Sessions are a stateful server-side approach to managing user data across multiple requests.

- **Storage Location:** User data (state) is stored on the **server** (in memory, a database, or a dedicated store like Redis).
- **Client Link:** The client is issued a unique **Session ID**, typically stored in a secure, `HttpOnly` cookie.
- **Stateful:** Since the server stores the session data, the server must maintain state for every active user, which can limit horizontal scaling.
- **Session Expiration:**
  - **Idle Timeout:** The session is destroyed if no activity is detected for a specified period (e.g., 30 minutes). This is a security measure.
  - **Absolute Timeout:** The session is destroyed after a fixed total duration, regardless of user activity, forcing a re-login.

### Tokens (e.g., JWT)

Tokens are a stateless, client-side approach where all necessary information is encoded into a single string, most commonly implemented using **JSON Web Tokens (JWT)**.

- **Stateless:** The server does not need to store user state between requests; the token itself carries all necessary data (**claims**), such as the user ID and permissions.
- **Verification:** Tokens are cryptographically **signed** by the server's secret key. The server validates the signature on every request to ensure the token hasn't been tampered with.
- **Storage and Transmission:** Tokens are typically stored in the browser's local storage or in memory, and transmitted in the **`Authorization` header** (`Bearer <token>`) rather than automatically via cookies.
- **Revocation Challenge:** Since they are stateless, revoking a token before its natural expiration requires extra complexity, such as implementing a **blocklist (denylist)** on the server or using short expiration times paired with refresh tokens.

---

## **How do JWTs work?**

A **JWT (JSON Web Token)** is a compact, URL-safe means of representing claims to be transferred between two parties. It consists of three parts separated by dots (`.`), all of which are Base64Url-encoded.

### 1. Header

The Header is a JSON object that specifies the type of the token and the cryptographic algorithm used for the signature.

- **Structure:** Typically contains two fields: `typ` (Type, usually set to `JWT`) and `alg` (Algorithm, e.g., `HS256` or `RS256`).
- **Encoding:** The JSON is **Base64Url-encoded** to form the first part of the JWT string.
- **Example:** `{"alg": "HS256", "typ": "JWT"}`

### 2. Payload (Claims)

The Payload is a JSON object that contains the "claims," or statements about an entity (typically the user) and additional data. Claims are the vital pieces of information the token carries.

- **Registered Claims:** Pre-defined, optional, but recommended claims to provide useful interoperability.
  - **`iss` (Issuer):** Who issued the token.
  - **`exp` (Expiration Time):** The time after which the token is invalid (crucial for security).
  - **`sub` (Subject):** The principal (user or service) the token refers to.
- **Public Claims:** Claims defined by those using JWTs, meant to be registered in the IANA registry, or defined in the application's configuration.
- **Private Claims:** Custom claims created to share information between the parties. _Example: user roles or internal IDs._
- **Encoding:** The JSON is **Base64Url-encoded** to form the second part of the JWT string.

### 3. Signature

The Signature is used to verify that the sender of the JWT is who they claim to be and to ensure the token hasn't been tampered with during transit.

- **Creation Process:**
  1.  Take the Base64Url-encoded **Header**.
  2.  Take the Base64Url-encoded **Payload**.
  3.  Concatenate them with a dot: `header.payload`.
  4.  Run this string through the specified algorithm (from the header) using a secret key known _only_ to the server.
- **Verification:** When the server receives the token, it recalculates the signature using the header, payload, and its secret key. If the calculated signature matches the signature provided in the token, the token is considered **valid**.

### Token Lifecycle

The server issues the token after a successful authentication. The client includes it in subsequent requests, usually in the **`Authorization` header** using the **`Bearer` scheme**. The server verifies the signature and extracts the claims from the payload without needing to consult a database for session state.

---

## **Rate Limiting**

Rate limiting controls how many requests a client (IP, user, or API key) can make within a time window to prevent abuse or overload. Common strategies include:

- **Fixed Window:** Simple counter per interval (e.g., 100/minute).
- **Sliding Window:** Smoother enforcement by checking recent timestamps.
- **Token Bucket:** Allows bursts while maintaining an average rate.
- **Leaky Bucket:** Queues requests and processes at a steady rate.

It can be applied at:

- **Infrastructure Level:** Nginx, API gateways, Cloudflare (best for scale).
- **Application Level:** Middleware/decorators in Django or FastAPI.
- **Shared Cache:** Redis for distributed state across servers.

When limits are exceeded, return **HTTP 429 (Too Many Requests)** with headers like:

```
X-RateLimit-Limit, X-RateLimit-Remaining, Retry-After
```

Best practices: use different limits for user tiers, prefer Redis or infra-based enforcement, and ensure atomic counters to avoid race conditions.

---

## **What are middleware and interceptors**

**Middleware** is software that sits between the client request and the server response, processing requests or responses. In Python frameworks like Django, middleware can handle authentication, logging, or request modification.
**Interceptors** (common in frameworks like Flask, FastAPI, or DRF) are similar but often more fine-grained, allowing pre- and post-processing of requests/responses for specific routes or controllers.

---

## **What is pagination in APIs**

Pagination divides large datasets into smaller chunks (pages) to reduce payload size and improve performance. Common approaches include:

- **Offset-based**: Use `limit` and `offset` query parameters
- **Cursor-based**: Use a cursor token to fetch the next page, more efficient for large datasets
- **Page-based**: Simple `page` and `per_page` parameters

---

## **OWASP (Open Web Application Security Project)**

**OWASP** is a nonprofit foundation dedicated to improving web application security. It provides open-source tools, documentation, and standards widely used across the industry. The most notable is the **OWASP Top 10**, a regularly updated list of the most critical security risks for web applications.

### **OWASP Top 10 (2021 Edition — Common Core Concepts)**

#### 1. **Broken Access Control**

When users can perform actions or access data beyond what they’re authorized to.

- **Example:** A normal user can access `/admin` endpoints.
- **Mitigation:** Enforce role-based permissions on the backend, validate authorization at every layer.

#### 2. **Cryptographic Failures**

Sensitive data (passwords, tokens, credit cards) is not properly protected.

- **Example:** Storing passwords in plain text or using weak encryption.
- **Mitigation:** Always use modern algorithms (e.g., AES-256, bcrypt, Argon2), enable HTTPS, avoid custom crypto.

#### 3. **Injection**

User input is passed directly into a command, query, or interpreter (SQL, NoSQL, OS commands).

- **Example:** `SELECT * FROM users WHERE name = '{input}'` → SQL injection.
- **Mitigation:** Use parameterized queries or ORM methods; never concatenate user input into queries.

#### 4. **Insecure Design**

Poorly designed features that inherently allow security flaws.

- **Example:** A “Forgot Password” feature without rate limiting or token expiration.
- **Mitigation:** Security must be part of system design — use threat modeling and security design patterns.

#### 5. **Security Misconfiguration**

Default, incomplete, or unnecessary configurations that expose data or systems.

- **Example:** Debug mode enabled in production, open S3 buckets, verbose error messages.
- **Mitigation:** Disable debug, enforce least privilege, and use configuration management tools.

#### 6. **Vulnerable and Outdated Components**

Using outdated libraries, frameworks, or packages with known vulnerabilities.

- **Mitigation:** Regularly patch dependencies, use tools like `pip-audit`, `safety`, or GitHub Dependabot.

#### 7. **Identification and Authentication Failures**

Weak login systems, session handling, or password management.

- **Example:** No account lockout, predictable tokens, or missing session invalidation.
- **Mitigation:** Use secure session tokens, MFA, and proper password storage (bcrypt/Argon2).

#### 8. **Software and Data Integrity Failures**

Using untrusted data sources or libraries without verifying integrity.

- **Example:** Installing unsigned dependencies from random URLs.
- **Mitigation:** Verify package signatures, use trusted repositories, and signed updates.

#### 9. **Security Logging and Monitoring Failures**

Lack of audit logs or alerting for suspicious activity.

- **Example:** Brute-force attacks go unnoticed.
- **Mitigation:** Log authentication events, access violations, and implement monitoring/alerting systems.

#### 10. **Server-Side Request Forgery (SSRF)**

The server makes HTTP requests to user-specified URLs without validation.

- **Example:** File fetch endpoint allows access to internal metadata URLs.
- **Mitigation:** Validate and restrict outbound requests, block internal IP ranges, use allowlists.

# Django Blog API

A robust, feature-rich RESTful API for a blogging platform built with Django 5 and Django REST Framework. This project demonstrates modern backend development practices, including JWT authentication, optimized database queries, and comprehensive documentation.

## 🚀 Features

*   **User Management**: Secure signup and login with JWT authentication (Access & Refresh tokens).
*   **CRUD Operations**: Full Create, Read, Update, and Delete capabilities for Posts and Tags.
*   **Advanced Content Features**:
    *   **Read Time Calculation**: Automatically estimates reading time for posts.
    *   **Tagging System**: Organize posts with a flexible tagging system.
*   **Search & Filtering**:
    *   Full-text search on titles and content.
    *   Filter by Author, Tags, and Titles.
    *   Pagination support for large datasets.
*   **Performance Optimization**: Solves the N+1 query problem using `select_related` and `prefetch_related`.
*   **Documentation**: Interactive Swagger/OpenAPI documentation.

## 🛠️ Tech Stack

*   **Framework**: Django 5.x
*   **API Toolkit**: Django REST Framework (DRF)
*   **Database**: PostgreSQL / SQLite (Default)
*   **Authentication**: Simple JWT
*   **Documentation**: drf-yasg (Swagger/Redoc)
*   **Utilities**: readtime, django-filter

## 📦 Installation & Setup

1.  **Clone the repository**
    ```bash
    git clone <repository-url>
    cd blog_api
    ```

2.  **Create a Virtual Environment**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

3.  **Install Dependencies**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Apply Migrations**
    ```bash
    python manage.py migrate
    ```

5.  **Run the Server**
    ```bash
    python manage.py runserver
    ```

6.  **Explore the API**
    *   Swagger UI: [http://127.0.0.1:8000/swagger/](http://127.0.0.1:8000/swagger/)
    *   ReDoc: [http://127.0.0.1:8000/redoc/](http://127.0.0.1:8000/redoc/)

## 🔑 Key Endpoints

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| **POST** | `/api/signup/` | Register a new user |
| **POST** | `/api/login/` | proper JWT login (obtain pair) |
| **GET** | `/api/post` | List all posts (Filterable) |
| **POST** | `/api/post` | Create a new post |
| **GET** | `/api/post/{uuid}` | Retrieve single post details |
| **PUT/PATCH** | `/api/post/{uuid}` | Update a post |
| **DELETE** | `/api/post/{uuid}` | Delete a post |

## 💡 Query Optimization Code Snippet
```python
# Efficiently fetching related objects to prevent N+1 Query problems
posts = Post.objects.select_related('author').prefetch_related('tag').all()
```

# 🛍️ Product & Category API Documentation

**Base URL**: `http://localhost:8000/api/`

---

## 🔐 AUTHENTICATION (JWT)

### 1. Obtain Token

**POST** `/token/`

**JSON Request:**

```json
{
  "username": "admin_username",
  "password": "admin_password"
}
```

**Response:**

```json
{
  "access": "<your_access_token>",
  "refresh": "<your_refresh_token>"
}
```

📌 Use the `access` token in all protected requests:

```
Authorization: Bearer <access_token>
```

---

## 🗂️ CATEGORY APIs

### 2. Create Category

**POST** `/categories/create/`

* Permission: Admin Only
* Content-Type: `multipart/form-data`

**Required Fields:**

* `name` (string, required)
* `image` (file, required)

**JSON Reference (for understanding):**

```json
{
  "name": "Shirts"
}
```

---

### 3. List Categories

**GET** `/categories/`

* Permission: Public
* No input needed.

---

### 4. Get Category Detail

**GET** `/categories/<id>/`

* Permission: Public

---

### 5. Update Category

**PUT** `/categories/<id>/update/`

* Permission: Admin Only
* Content-Type: `multipart/form-data`

**JSON Reference:**

```json
{
  "name": "Updated Category"
}
```

---

### 6. Delete Category

**DELETE** `/categories/<id>/delete/`

* Permission: Admin Only
* No body required

---

## 📦 PRODUCT APIs

### 7. Create Product

**POST** `/products/create/`

* Permission: Admin Only
* Content-Type: `multipart/form-data`

**Required Fields:**

```json
{
  "category_id": 1,
  "name": "Stylish Shirt",
  "product_type": "Casual",
  "fabric": "Cotton",
  "color": "Blue",
  "size": "medium",
  "product_code": "SS001",
  "stock_keeping_unit": "SKU001",
  "cost_price": "299.99",
  "wholesale_price": "249.99",
  "min_order_quantity": 5,
  "current_stock": 100,
  "allow_customization": true,
  "description": "Soft blue cotton casual shirt",
  "is_draft": false
}
```

> Upload image(s) using form-data key `images`

---

### 8. List Products

**GET** `/products/`

* Permission: Public

**Optional Query Parameters:**

* `?ordering=cost_price`
* `?ordering=-created_at`

---

### 9. Get Product Detail

**GET** `/products/<id>/`

* Permission: Public

---

### 10. Update Product

**PUT** `/products/<id>/update/`

* Permission: Admin Only
* Content-Type: `multipart/form-data`

**Example JSON Body (partial):**

```json
{
  "name": "Updated Shirt",
  "cost_price": "279.99",
  "current_stock": 120
}
```

> Upload new `images` (optional) using form-data.

---

### 11. Delete Product

**DELETE** `/products/<id>/delete/`

* Permission: Admin Only
* No body required

---

### 12. Upload Additional Images

**POST** `/products/<id>/upload_images/`

* Permission: Admin Only
* Content-Type: `multipart/form-data`

**Form-Data Field:**

* `images`: file(s)

---

### 13. Search Products

**GET** `/products/search/?search=shirt`

* Permission: Public

Searches by `name`, `product_code`, or `description`

---

### 14. Filter Products

**GET** `/products/filter/`

* Permission: Public

**Query Parameters:**

* `category` (Category ID)
* `size` (e.g., medium, large)
* `allow_customization` (true or false)

**Example:**

```
/products/filter/?category=1&size=medium&allow_customization=true
```

---

## 👤 Admin Setup

To access admin-only APIs:

1. Run `python manage.py createsuperuser`
2. Login at `/admin/` and use the credentials in `/token/` endpoint.
3. Use `access` token for protected routes.

---

## ✅ Permissions Summary

| Endpoint                       | Method | Auth Required | Notes  |
| ------------------------------ | ------ | ------------- | ------ |
| /categories/                   | GET    | ❌             | Public |
| /categories/create/            | POST   | ✅ Admin       |        |
| /categories/<id>/update/       | PUT    | ✅ Admin       |        |
| /categories/<id>/delete/       | DELETE | ✅ Admin       |        |
| /products/                     | GET    | ❌             | Public |
| /products/create/              | POST   | ✅ Admin       |        |
| /products/<id>/                | GET    | ❌             | Public |
| /products/<id>/update/         | PUT    | ✅ Admin       |        |
| /products/<id>/delete/         | DELETE | ✅ Admin       |        |
| /products/<id>/upload\_images/ | POST   | ✅ Admin       |        |
| /products/search/              | GET    | ❌             | Search |
| /products/filter/              | GET    | ❌             | Filter |

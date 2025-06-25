# Pizza Restaurants API and Frontend

## Overview

This project implements a simple restaurant–pizza ordering system with:

* **Backend**

A Flask RESTful API with three models (`Restaurant`, `Pizza`, `RestaurantPizza`) and full CRUD support for restaurants and restaurant\_pizzas, plus read-only for pizzas.
* **Frontend**

 A React app that consumes the API to list restaurants and pizzas, create new menu items, and delete restaurants.

---

## Installation & Setup

1. **Clone the repository**

   ```bash
   git clone https://github.com/PreeNJ/phase-4-pizza-challenge.git
   cd phase-4-pizza-challenge/server
   ```
2. **Create and activate a virtual environment**

   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```
3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```
4. **Initialize and migrate database**

   ```bash
   flask db init    # if running first time
   flask db migrate
   flask db upgrade
   ```
5. **Run the server**

   ```bash
   flask run
   ```
6. **Start frontend** (in separate terminal)

   ```bash
   cd ../frontend
   npm install
   npm start
   ```

---

## Database Models

### 1. Restaurant

* `id` (Integer, PK)
* `name` (String)
* `address` (String)
* **Associations**: `has_many :restaurant_pizzas`, `has_many :pizzas, through: :restaurant_pizzas`
* **Cascade Delete**: Deleting a restaurant removes associated `RestaurantPizza` records.

### 2. Pizza

* `id` (Integer, PK)
* `name` (String)
* `ingredients` (String)
* **Associations**: `has_many :restaurant_pizzas`, `has_many :restaurants, through: :restaurant_pizzas`
 

```
Restaurant <─┐            ┌─> Pizza
            └─ RestaurantPizza ─┘
```

---

## Validations

* **Restaurant**: `name` and `address` must be present
* **Pizza**: `name` and `ingredients` must be present
* **RestaurantPizza**: `price` must be present, integer, between `1` and `30`

---

## API Routes 

### GET /restaurants

* **Description**: Returns a list of all restaurants
* **Response**:

  ```json
  [
    {
      "id": 1,
      "name": "Joe's Diner",
      "address": "123 Main St",
      "restaurant_pizzas": [ ... ]
    },
    { ... }
  ]
  ```

### GET /restaurants/\:id

* **Description**: Returns a single restaurant by ID
* **Success (200)**:

  ```json
  {
    "id": 2,
    "name": "Pizza Palace",
    "address": "456 Elm Ave",
    "restaurant_pizzas": [
      { "id": 5, "price": 12, "pizza": { "id": 3, ... } }
    ]
  }
  ```
* **Not Found (404)**:

  ```json
  { "error": "Restaurant not found" }
  ```

### GET /pizzas

* **Description**: Returns a list of all pizzas
* **Response**:

  ```json
  [
    { "id": 1, "name": "Margherita", "ingredients": "tomato, mozzarella" },
    { "id": 2, "name": "Pepperoni", "ingredients": "tomato, mozzarella, pepperoni" }
  ]
  ```

### DELETE /restaurants/\:id 
* **Description**: Deletes a restaurant and cascades to its `RestaurantPizza` records
* **Success (204)**: No body
* **Not Found (404)**:

  ```json
  { "error": "Restaurant not found" }
  ```

### POST /restaurant\_pizzas  

* **Description**: Creates a new menu item linking a restaurant and a pizza
* **Request Body**:

  ```json
  { "restaurant_id": 1, "pizza_id": 2, "price": 18 }
  ```
* **Success (201)**:

  ```json
  { "id": 10, "price": 18, "pizza": {...}, "restaurant": {...} }
  ```
* **Validation Error (422)**:

  ```json
  { "errors": ["Price must be between 1 and 30"] }
  ```

---

## Frontend (view)  
All operations are hooked up in the React app:

* **Listing**: On load, `App.js` fetches `/restaurants` and `/pizzas`, passing data into `RestaurantList` and `PizzaList` components.
* **Create Menu Item**: `PizzaForm.js` controls a form for `restaurant_id`, `pizza_id`, and `price`; on submit, posts to `/restaurant_pizzas`, then updates the view.
* **Delete Restaurant**: `Restaurant.js` renders a delete button; clicking it calls `DELETE /restaurants/:id` and removes the restaurant from state.

 

## License

© Priscillah Njai

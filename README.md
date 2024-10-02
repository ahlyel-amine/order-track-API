# Project Structure and API Routes

## Introduction
This document outlines the project structure, necessary API endpoints, and other important details about the API. The API supports various roles with access to different functionalities, allowing users to manage menu items, place orders, assign delivery crews, and track order deliveries.

## Scope
The API is designed to enable developers to create web and mobile applications. The system supports users with different roles, such as managers and delivery crew, allowing them to browse, edit menu items, place and track orders, and manage deliveries.

## Project Structure
The project consists of a single Django application named `API`. All required API endpoints are implemented within this app. Dependencies are managed using `pipenv` in a virtual environment to ensure a clean and isolated project setup.

## API Design

### Function-Based and Class-Based Views
The API supports both function-based and class-based views, following proper naming conventions throughout the project. Both approaches are used to provide flexibility in handling different API routes and ensuring maintainability.

### User Groups
The project defines two user groups:
- **Manager**: Users who can manage menu items and assign delivery crews.
- **Delivery Crew**: Users responsible for delivering orders.

Users who are not assigned to any group are considered customers, and their access is restricted accordingly.

### Error Handling and Status Codes
The API provides appropriate HTTP status codes for different scenarios, including successful requests and error conditions:

| HTTP Status Code      | Description                                      |
| --------------------- | ------------------------------------------------ |
| **200 - Ok**          | Returned for all successful `GET`, `PUT`, `PATCH`, and `DELETE` requests. |
| **201 - Created**     | Returned for successful `POST` requests.          |
| **403 - Unauthorized**| Returned when authorization fails for the current user token. |
| **401 - Forbidden**   | Returned when authentication fails.              |
| **400 - Bad Request** | Returned for validation errors in `POST`, `PUT`, `PATCH`, and `DELETE` requests. |
| **404 - Not Found**   | Returned when a resource is not found.            |

## API Endpoints

### User Registration and Token Management
The API provides endpoints to handle user registration and token management. Djoser is used to simplify user authentication and token generation processes.

| Endpoint                | Method | Role                        | Description                                      |
| ----------------------- | ------ | --------------------------- | ------------------------------------------------ |
| `/api/users`            | POST   | Public                      | Creates a new user with name, email, and password. |
| `/api/users/me/`        | GET    | Authenticated users          | Returns the current user profile.                |
| `/token/login/`         | POST   | Public                      | Generates an access token for future API requests. |

### Menu Items Management
The API provides endpoints for managing menu items, including listing, adding, updating, and deleting items. Access is restricted based on the user's role.

| Endpoint                          | Method | Role                  | Description                                      |
| ---------------------------------- | ------ | --------------------- | ------------------------------------------------ |
| `/api/menu-items`                 | GET    | Customer, Delivery Crew | Lists all menu items.                            |
| `/api/menu-items`                 | POST, PUT, PATCH, DELETE | Customer, Delivery Crew | Denies access with `403 Unauthorized`. |
| `/api/menu-items/{menuItem}`      | GET    | Customer, Delivery Crew | Lists a single menu item.                        |
| `/api/menu-items`                 | POST   | Manager               | Creates a new menu item.                         |
| `/api/menu-items/{menuItem}`      | PUT, PATCH, DELETE | Manager | Updates or deletes a specific menu item.         |

### User Group Management
The API allows managers to assign users to groups and manage the users within the Manager and Delivery Crew groups.

| Endpoint                               | Method | Role       | Description                                      |
| -------------------------------------- | ------ | ----------| ------------------------------------------------ |
| `/api/groups/manager/users`            | GET    | Manager   | Lists all users in the Manager group.            |
| `/api/groups/manager/users`            | POST   | Manager   | Assigns a user to the Manager group.             |
| `/api/groups/delivery-crew/users`      | GET    | Manager   | Lists all users in the Delivery Crew group.      |
| `/api/groups/delivery-crew/users`      | POST   | Manager   | Assigns a user to the Delivery Crew group.       |

### Cart Management
Customers can manage their cart by adding or removing items. The API provides endpoints for viewing and modifying the cart.

| Endpoint                          | Method | Role       | Description                                      |
| ---------------------------------- | ------ | ----------| ------------------------------------------------ |
| `/api/cart/menu-items`            | GET    | Customer   | Lists all items in the current user's cart.      |
| `/api/cart/menu-items`            | POST   | Customer   | Adds a new item to the cart.                     |
| `/api/cart/menu-items`            | DELETE | Customer   | Removes all items from the cart.                 |

### Order Management
The API provides robust order management for both customers and managers, allowing users to place orders and track their status.

| Endpoint                          | Method | Role       | Description                                      |
| ---------------------------------- | ------ | ----------| ------------------------------------------------ |
| `/api/orders`                     | GET    | Customer   | Lists all orders created by the current user.    |
| `/api/orders`                     | POST   | Customer   | Creates a new order using the items from the user's cart. |
| `/api/orders/{orderId}`           | GET    | Customer   | Retrieves details for a specific order.          |
| `/api/orders/{orderId}`           | PUT, PATCH | Manager | Updates the order, assigns delivery crew, and changes the status. |
| `/api/orders/{orderId}`           | DELETE | Manager   | Deletes an order.                                |
| `/api/orders`                     | GET    | Delivery Crew | Lists all orders assigned to the delivery crew.  |

## Additional Features
- **Filtering, Pagination, and Sorting**: Implemented for `/api/menu-items` and `/api/orders` endpoints to handle large data sets efficiently.
- **Throttling**: Rate limiting is applied to authenticated and unauthenticated users to prevent abuse of the API.

---

This API project provides all the required endpoints to manage menu, user roles, orders, and cart functionalities. Each endpoint ensures proper role-based access control, error handling, and the use of appropriate HTTP status codes for a smooth user experience.

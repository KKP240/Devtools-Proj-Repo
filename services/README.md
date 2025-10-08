Microservices layout

- services/user_service: JWT auth and user management (Django default User)
- services/pet_service: Pet CRUD owned by user_id
- services/booking_service: Bookings and reviews using user_id and pet_id references

All services use the same shared JWT signing secret so tokens from user_service are accepted by others.

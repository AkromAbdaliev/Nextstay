from fastapi import HTTPException, status

UserAlreadyExistsException = HTTPException(
    status_code=status.HTTP_409_CONFLICT, detail="User already exists"
)

InvalidCredentialsException = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password"
)

TokenExpiredException = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED, detail="Token has expired"
)

UnauthorizedException = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized"
)

InvalidTokenFormatException = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token format"
)

UserNotFoundException = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
)

HotelNotFoundException = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND, detail="Hotel not found"
)

RoomNotFoundException = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND, detail="Room not found"
)

BookingNotFoundException = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND, detail="Booking not found"
)

RoomCannotBeBookedException = HTTPException(
    status_code=status.HTTP_409_CONFLICT, detail="Room cannot be booked"
)

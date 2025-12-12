from email.message import EmailMessage

from pydantic import EmailStr

from app.core.config import settings


def create_booking_confirmation(booking: dict, email_to: EmailStr) -> EmailMessage:
    email = EmailMessage()
    email["Subject"] = "Booking Confirmation"
    email["From"] = settings.SMTP_USER
    email["To"] = email_to

    html_content = f"""
    <!DOCTYPE html>
    <html>
      <body style="font-family: 'Arial', sans-serif; background-color: #f4f4f7; margin: 0; padding: 0;">
        <div style="max-width: 600px; margin: auto; background-color: #ffffff; padding: 20px; border-radius: 8px; box-shadow: 0 0 10px rgba(0,0,0,0.1);">
          
          <h2 style="color: #2e86de; text-align: center;">Nextstay</h2>
          <p style="font-size: 16px; color: #333;">Hello,</p>
          <p style="font-size: 16px; color: #333;">
            Thank you for booking with our service! Here are your booking details:
          </p>

          <table style="width: 100%; border-collapse: collapse; margin: 20px 0;">
            <tr>
              <td style="padding: 8px; font-weight: bold;">Hotel:</td>
              <td style="padding: 8px;">{booking.get('hotel_id', 'Your Hotel')}</td>
            </tr>
            <tr>
              <td style="padding: 8px; font-weight: bold;">Check-in:</td>
              <td style="padding: 8px;">{booking['date_from']}</td>
            </tr>
            <tr>
              <td style="padding: 8px; font-weight: bold;">Check-out:</td>
              <td style="padding: 8px;">{booking['date_to']}</td>
            </tr>
            <tr>
              <td style="padding: 8px; font-weight: bold;">Total Price:</td>
              <td style="padding: 8px;">${booking['total_cost']}</td>
            </tr>
          </table>

          <p style="text-align: center; margin: 30px 0;">
            <a href="{booking.get('booking_link', '#')}" 
               style="background-color: #2e86de; color: white; padding: 12px 24px; text-decoration: none; border-radius: 5px; font-weight: bold;">
               View Booking
            </a>
          </p>

          <p style="font-size: 14px; color: #999; text-align: center;">
            If you did not make this booking, please contact our support immediately.
          </p>

          <p style="text-align: center; font-size: 12px; color: #bbb;">
            &copy; 2025 Nextstay. All rights reserved.
          </p>
        </div>
      </body>
    </html>
    """

    email.set_content(html_content, subtype="html")
    return email

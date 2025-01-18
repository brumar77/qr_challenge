import pytest
from app.src.models.users import User

@pytest.mark.parametrize("qr_data, expected_status", [
    (
        {
            "url": "https://www.lacoste.com/",
            "color": "#000000",
            "size": 150,
            "user_id": None,
        },
        200,
    ),
    (
        {
            "url": "https://udemy.com",
            "color": "#000000",
            "size": 150,
            "user_id": "00000000-0000-0000-0000-000000000000",
        },
        404,
    ),
])
@pytest.mark.qr
def test_create_qr_code(qr_data, expected_status, test_client, test_db, test_user, auth_headers):
    """Prueba del endpoint para crear códigos QR."""
    if qr_data["user_id"] is None:
        user = test_db.query(User).filter_by(email=test_user["user_email"]).first()
        test_db.refresh(user)
        qr_data["user_id"] = str(user.id)

    response = test_client.post(
        "/user/qr-codes/", 
        json=qr_data,
        headers=auth_headers
    )

    assert response.status_code == expected_status

    if response.status_code == 200:
        assert response.headers["Content-Type"] == "image/png"
        assert response.headers["Content-Disposition"].startswith("attachment; filename=qr_code.png")
    elif response.status_code == 404:
        assert response.json() == {"detail": "User not found"}
    elif response.status_code == 500:
        assert response.json() == {"detail": "Error generating QR code"}
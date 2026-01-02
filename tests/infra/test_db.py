from sqlalchemy import select
from dataclasses import asdict
import pytest
from fast_auth.models import User


@pytest.mark.asyncio
async def test_create_user(session, mock_db_time):
    with mock_db_time(model=User) as time: 
        new_user = User(
            username='alice', password='secret'
        )
        session.add(new_user)
        await session.commit()

    user = await session.scalar(select(User).where(User.username == 'alice'))

    assert asdict(user) == { 
        'id': 1,
        'username': 'alice',
        'password': 'secret',
        'created_at': time,  
    }
from app.domain.entities.donor import Donor


def test_donor_creation():
    donor = Donor.create(
        donor_id=None,
        znumber=12345,
        name="Ross",
        age=30,
        region="NY",
        other_factors={}
    )

    assert donor.name == "Ross"
    # ZNumber wraps value; compare using int() if present
    if hasattr(donor.znumber, "__int__"):
        assert int(donor.znumber) == 12345
    else:
        assert donor.znumber == 12345

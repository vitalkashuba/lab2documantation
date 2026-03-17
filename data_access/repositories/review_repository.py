class ReviewRepository:

    def __init__(self, session):
        self.session = session

    def add_review(self, review):
        self.session.add(review)

    def save(self):
        self.session.commit()
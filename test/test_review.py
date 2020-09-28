from app.models import Review,User
from app import db

def setUp(self):
    self.user_nelly = User(username = 'nelly',password = 'potato', email = 'nelly@gmail.com')
    self.new_review = Review(blog_id=12345,blog_title='Review for bloges',image_path="https://image.tmdb.org/t/p/w500/jdjdjdjn",blog_review='This blog is the best thing since sliced bread',user = self.user_nelly )

def tearDown(self):
    Review.query.delete()
    User.query.delete()

def test_check_instance_variables(self):
    self.assertEquals(self.new_review.blog_id,12345)
    self.assertEquals(self.new_review.blog_review,'This blog is the best thing since sliced bread')
    self.assertEquals(self.new_review.user,self.user_nelly)

def test_save_review(self):
    self.new_review.save_review()
    self.assertTrue(len(Review.query.all())>0)

def test_get_review_by_id(self):
    self.new_review.save_review()
    got_reviews = Review.get_reviews(12345)
    self.assertTrue(len(got_reviews) == 1)
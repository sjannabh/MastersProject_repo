import ReviewModel from '../models/reviewModel/reviewSchema.js';

//get all reviews
export const getReviews = async (req, res) => {
    await ReviewModel.find({})
        .then(allReviews => { console.log(allReviews); res.json(allReviews); })
        .catch(err => { console.log(err); res.json(err); });

};

//get single review
export const getReview = (req, res) => {
    const review_id = req.params.id;

    const review = ReviewModel.findOne({ review_id })
        .then(review => { console.log(review); res.json(review); })
        .catch(err => { console.log(err); res.json(err); })
};

//create a review
export const createReview = async (req, res) => {
    const review = req.body;
    const doc = new ReviewModel({ ...review })
    await doc.save();
    res.send('Review Created Successfully')
};

//updata a review
export const updateReview = async (req, res) => {
    const _id = req.params.id;

    const review = await ReviewModel.findByIdAndUpdate(_id, req.body, { new: true })
        .then(console.log("Review updated"))
        .catch((err) => console.log(err))
    res.send('Review Updated Successfully');
};

// delete a review
export const deleteReview = async (req, res) => {
    try {
        const _id = req.params.id;

        const review = await ReviewModel.findByIdAndDelete(_id)
            .then(console.log("Review deleted"))
            .catch((err) => console.log(err))

    }
    catch (error) {
        res.status(500).json({ message: error.message })
    }
    res.send('Review Deleted Successfully')
}
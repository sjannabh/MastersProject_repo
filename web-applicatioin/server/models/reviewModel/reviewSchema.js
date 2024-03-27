import mongoose from "mongoose";

const reviewSchema = new mongoose.Schema({
    product_id: { type: String },
    user_id: { type: String },
    review_id: { type: String },
    review_title: { type: String },
    review_content: { type: String },
});

const ReviewModel = mongoose.model("review", reviewSchema);

export default ReviewModel;

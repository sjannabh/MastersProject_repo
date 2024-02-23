import express from 'express'
import { getReviews, createReview, getReview, deleteReview, updateReview } from '../../controllers/reviews.js';


const reviewRouter = express.Router();

reviewRouter.get("/reviews", getReviews);
reviewRouter.post("/review", createReview);
reviewRouter.get("/review/:id", getReview);
reviewRouter.delete("/review/:id", deleteReview);
reviewRouter.put("/review/:id", updateReview);

export default reviewRouter;
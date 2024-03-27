import mongoose from "mongoose";

const productSchema = new mongoose.Schema({
    product_id: { type: String },
    product_name: { type: String },
    category: { type: Array },
    price: { type: Number },
    img_link: { type: String },
    product_link: { type: String },
    product_description: { type: String },
    rating: { type: Number },
    no_of_ratings: { type: Number },
});

const ProductModel = mongoose.model("product", productSchema);

export default ProductModel;

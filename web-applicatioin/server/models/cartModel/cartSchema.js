import mongoose from "mongoose";

const cartSchema = new mongoose.Schema({
    cart_id: { type: String },
    product_id: { type: String },
    product_name: { type: String },
    category: { type: Array },
    img_link: { type: String },
    product_link: { type: String },
});

const CartModel = mongoose.model("cart", cartSchema);

export default CartModel;

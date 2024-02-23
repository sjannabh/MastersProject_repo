import mongoose from 'mongoose'

const orderSchema = new mongoose.Schema({
    cart_id: { type: String },
    product_id: { type: String },
    product_name: { type: String },
    category: { type: Array },
    img_link: { type: String },
    product_link: { type: String },
    price: { type: Number },
    user_id: { type: String },
    billing_address: {
        first_name: {type:String},
        last_name: {type:String},
        address_1: {type:String},
        address_2: {type:String},
        city:{type:String},
        state:{type:String},
        zipcode:{type:Number}
    }
})

const OrderModel = mongoose.model('order_data', orderSchema)

export default OrderModel
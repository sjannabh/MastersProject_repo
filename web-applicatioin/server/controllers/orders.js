import OrderModel from '../models/OrderModel/orderSchema.js';

//get all users
export const getAllOrders = async (req, res) => {

    await OrderModel.find({})
        .then(allitems => { console.log(allitems); res.json(allitems); })
        .catch(err => { console.log(err); res.json(err); });

};

// get single user
export const getSingleOrder = (req, res) => {

    const _id = req.params.id;

    const item = OrderModel.findById({ _id })
        .then(item => { console.log(item); res.json(item); })
        .catch(err => { console.log(err); res.json(err); })


};

export const updateOrder = async (req, res) => {

    const _id = req.params.id;

    const item = await OrderModel.findByIdAndUpdate(_id, req.body, { new: true })
        .then(console.log("order updated"))
        .catch((err) => console.log(err))
    res.send('order Updated Successfully');
}

//delete single user
export const deleteOrder = async (req, res) => {

    try {
        const _id = req.params.id;

        const item = await OrderModel.findByIdAndDelete(_id)
            .then(console.log("order deleted"))
            .catch((err) => console.log(err))

    }
    catch (error) {
        res.status(500).json({ message: error.message })
    }
    res.send('Order Deleted Successfully')
};

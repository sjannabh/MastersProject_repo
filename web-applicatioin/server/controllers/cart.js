import CartModel from '../models/cartModel/cartSchema.js';

//get all users
export const getAllCartItems = async (req, res) => {

    await CartModel.find({})
        .then(allitems => { console.log(allitems); res.json(allitems); })
        .catch(err => { console.log(err); res.json(err); });

};

// get single user
export const getSingleCartItem = (req, res) => {

    const _id = req.params.id;

    const item = CartModel.findById({ _id })
        .then(item => { console.log(item); res.json(item); })
        .catch(err => { console.log(err); res.json(err); })


};

export const createCart = async (req, res) => {
    const item = req.body;
    const doc = new CartModel({ ...item })
    await doc.save();
    res.send('Item Created Successfully')
};

export const updateSingleCartItem = async (req, res) => {

    const _id = req.params.id;

    const item = await CartModel.findByIdAndUpdate(_id, req.body, { new: true })
        .then(console.log("item updated"))
        .catch((err) => console.log(err))
    res.send('item Updated Successfully');
}

//delete single user
export const deleteSingleCartItem = async (req, res) => {

    try {
        const _id = req.params.id;

        const item = await CartModel.findByIdAndDelete(_id)
            .then(console.log("item deleted"))
            .catch((err) => console.log(err))

    }
    catch (error) {
        res.status(500).json({ message: error.message })
    }
    res.send('Item Deleted Successfully')
};

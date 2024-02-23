import ProductModel from '../models/productModel/productSchema.js';

//get all users
export const getProducts = async (req, res) => {

    await ProductModel.find({})
        .then(allProducts => { console.log(allProducts); res.json(allProducts); })
        .catch(err => { console.log(err); res.json(err); });

};

// get single user
export const getProduct = (req, res) => {

    const _id = req.params.id;

    const product = ProductModel.findById({ _id })
        .then(product => { console.log(product); res.json(product); })
        .catch(err => { console.log(err); res.json(err); })
};

// create new user
export const createProduct = async (req, res) => {
    const product = req.body;
    const doc = new ProductModel({ ...product })
    await doc.save();
    res.send('Product Created Successfully')
};


// update single user
export const updateProduct = async (req, res) => {

    const _id = req.params.id;

    const product = await ProductModel.findByIdAndUpdate(_id, req.body, { new: true })
        .then(console.log("Product updated"))
        .catch((err) => console.log(err))
    res.send('Product Updated Successfully');
}

//delete single user
export const deleteProduct = async (req, res) => {

    try {
        const _id = req.params.id;

        const product = await ProductModel.findByIdAndDelete(_id)
            .then(console.log("Product deleted"))
            .catch((err) => console.log(err))

    }
    catch (error) {
        res.status(500).json({ message: error.message })
    }
    res.send('Product Deleted Successfully')
};

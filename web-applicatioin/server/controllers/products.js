import ProductModel from "../models/productModel/productSchema.js";

//get all products
export const getProducts = async (req, res) => {
    await ProductModel.find({})
        .then((allProducts) => {
            res.status(200).json(allProducts);
        })
        .catch((err) => {
            res.status(400).json(err);
        });
};

//get all products by name
export const getProductsByName = async (req, res) => {
    const name = req.params.name;
    const count = req.params.count;

    await ProductModel.find({})
        .then((allProducts) => {
            const results = allProducts.filter((product) => product.product_name.toLowerCase().includes(name.toLowerCase())).slice(0, count);
            res.status(200).json(results);
        })
        .catch((err) => {
            res.status(400).json(err);
        });
};

// get single product by product Id
export const getProduct = (req, res) => {
    const product_id = req.params.id;

    const product = ProductModel.findOne({ product_id })
        .then((product) => {
            res.status(200).json(product);
        })
        .catch((err) => {
            res.status(400).json(err);
        });
};

// create new product
export const createProduct = async (req, res) => {
    const product = req.body;
    const doc = new ProductModel({ ...product });
    await doc.save();
    res.send("Product Created Successfully");
};

// update single user
export const updateProduct = async (req, res) => {
    const product_id = req.params.id;

    const product = await ProductModel.findByIdAndUpdate(product_id, req.body, { new: true })
        .then(console.log("Product updated"))
        .catch((err) => console.log(err));
    res.send("Product Updated Successfully");
};

//delete single user
export const deleteProduct = async (req, res) => {
    try {
        const _id = req.params.id;

        const product = await ProductModel.findByIdAndDelete(_id)
            .then(console.log("Product deleted"))
            .catch((err) => console.log(err));
    } catch (error) {
        res.status(500).json({ message: error.message });
    }
    res.send("Product Deleted Successfully");
};

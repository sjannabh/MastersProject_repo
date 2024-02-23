import UserModel from '../models/userModel/userSchema.js';

//get all users
export const getUsers = async (req, res) => {

    await UserModel.find({})
        .then(allUsers => { console.log(allUsers); res.json(allUsers); })
        .catch(err => { console.log(err); res.json(err); });

};

// get single user
export const getUser = (req, res) => {

    const _id = req.params.id;

    const user = UserModel.findById({ _id })
        .then(user => { console.log(user); res.json(user); })
        .catch(err => { console.log(err); res.json(err); })
};

// create new user
export const createUser = async (req, res) => {
    const user = req.body;
    const doc = new UserModel({ ...user })
    await doc.save();
    res.send('User Created Successfully')
};

export const userSignin = async (req, res) => {
    const { email, password } = req.body;
    UserModel.findOne({ email: email })
        .then(user => {
            if (user) {
                if (user.password === password) {
                    res.json(user)
                } else {
                    res.status(401).json("The password is incorrect")
                }
            } else {
                res.status(404).json("no record is found")
            }
        })
}


// update single user
export const updateUser = async (req, res) => {

    const _id = req.params.id;

    const user = await UserModel.findByIdAndUpdate(_id, req.body, { new: true })
        .then(console.log("User updated"))
        .catch((err) => console.log(err))
    res.send('User Updated Successfully');
}

//delete single user
export const deleteUser = async (req, res) => {

    try {
        const _id = req.params.id;

        const user = await UserModel.findByIdAndDelete(_id)
            .then(console.log("User deleted"))
            .catch((err) => console.log(err))

    }
    catch (error) {
        res.status(500).json({ message: error.message })
    }
    res.send('User Deleted Successfully')
};

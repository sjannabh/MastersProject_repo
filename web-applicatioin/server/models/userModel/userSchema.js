import mongoose from 'mongoose';

const userSchema = new mongoose.Schema({
    user_id: { type: String },
    fname: { type: String },
    lname: { type: String },
    phoneNo: { type: String },
    email: { type: String },
    password: { type: String }
})

const UserModel = mongoose.model('UserData', userSchema)

export default UserModel
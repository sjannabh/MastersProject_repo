
import mongoose from 'mongoose';

const browsingHistorySchema = new mongoose.Schema({
    user_id: {type:String},
    product_list : {type:Array}
})

const BrowsingHistoryModel = mongoose.model('browsingHistory_data', browsingHistorySchema)

export default BrowsingHistoryModel
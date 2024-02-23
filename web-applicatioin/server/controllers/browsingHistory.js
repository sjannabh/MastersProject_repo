import BrowsingHistoryModel from '../models/browsingHistoryModel/browsingHistorySchema.js';

// get the browsing history of single user

export const getBrowsingHistory = async (req, res) => {

    const user_id = req.params.id;

    const products = await BrowsingHistoryModel.findById({ user_id })
        .then(product => { console.log(product); res.json(product); })
        .catch(err => { console.log(err); res.status(400).json(err); })
};

export const createAndUpdateHistory = (req, res) => {


    const user_id = req.body.user_id;

    const newRecord = req.body

    let data = BrowsingHistoryModel.findById({ user_id });

    console.log("data =>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>");
    console.log(data);
    if (data === null) {
        // craete a new record with user Id
        const doc = new BrowsingHistoryModel({ ...newRecord })
        doc.save();
        res.send('Browsing History Created Successfully')
    }
    else {
        // update the prudt information for that record
        const product = BrowsingHistoryModel.findByIdAndUpdate(user_id, newRecord, { new: true })
        res.send('user product updated successfully')

    }

}
import axios from "axios";

const QueryData = async () => {
    const res = await axios.get("http://127.0.0.1:5000/dummy_query")
    if (res == null){
        console.log("oops")
        return;
    }
    else{
        console.log(res.data)
    }
    return res.data;
};

export default {
    QueryData
};

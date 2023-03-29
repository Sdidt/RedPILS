import axios from "axios";

const QueryData = async () => {
    const res = await axios.get("http://127.0.0.1:5000/dummy_query")
    // const res = await axios.get("http://localhost:5000/dummy_query")
    if (res == null){
        console.log("oops")
        return;
    }
    else{
        console.log(res.data)
    }
    const res_data = res.data
    return res_data;
};

const export_const = {
    QueryData
}

export default export_const;

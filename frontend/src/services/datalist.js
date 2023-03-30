import axios from "axios";

const DummyQueryData = async () => {
    const res = await axios.get("http://127.0.0.1:5000/dummy_query")
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

const QueryStatsData = async () => {
    const res = await axios.get("http://127.0.0.1:5000//dummy_charts2d")
    console.log(res)
    if (res == null){
        console.log("oops")
        return;
    }
    else{
        console.log(res.data)
    }
    const res_data = res.data
    return res_data;
}

const QueryData = async (searchTerm,timeSelectConst) => {
    console.log(timeSelectConst)
    let res
    if(timeSelectConst!="All"){
        const whitespaceRemoved = searchTerm.replace(/\s/g, '+')
        res = await axios.get("http://127.0.0.1:5000/query?query="+whitespaceRemoved+"&timeframe="+timeSelectConst)
    }
    else{
        const whitespaceRemoved = searchTerm.replace(/\s/g, '+')
        res = await axios.get("http://127.0.0.1:5000/query?query="+whitespaceRemoved)
    }
    console.log(res)
    if (res == null){
        console.log("oops")
        return;
    }
    else{
        console.log(res.data)
    }
    const res_data = res.data
    return res_data;
}

const export_const = {
    QueryData,
    QueryStatsData
}

export default export_const;

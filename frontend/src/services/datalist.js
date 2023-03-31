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

const QueryData = async (searchTerm,timeSelectConst,locationName) => {
    console.log(timeSelectConst)
    let res
    const concatenateLocationName = locationName.join(' OR ');
    console.log(concatenateLocationName)
    if(timeSelectConst!="All" && concatenateLocationName!=[]){
        const whitespaceRemoved = searchTerm.replace(/\s/g, '+')
        res = await axios.get("http://127.0.0.1:5000/query?query="+whitespaceRemoved+"&timeframe="+timeSelectConst+"&region="+concatenateLocationName)
    }
    else if(timeSelectConst!="All"){
        const whitespaceRemoved = searchTerm.replace(/\s/g, '+')
        res = await axios.get("http://127.0.0.1:5000/query?query="+whitespaceRemoved+"&timeframe="+timeSelectConst)
    }
    else if(concatenateLocationName!=[]){
        const whitespaceRemoved = searchTerm.replace(/\s/g, '+')
        res = await axios.get("http://127.0.0.1:5000/query?query="+whitespaceRemoved+"&region="+concatenateLocationName)
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

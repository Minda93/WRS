/*========================================================*/
/*
    scan_black node
 */
/*--------------------------------------------------------*/

const Init_ScanBlack_Param = async () => {
    try {
        const param = await paramScanBlack.Get();
        var obj = document.getElementsByName("ScanElement");
        if (param != null) {
            for (var item in param) {
                switch (item) {
                    case "middleY":
                        obj[0].value = parseInt(param.middleY);
                        obj[1].value = parseInt(param.middleY);
                        break
                    case "range":
                        obj[2].value = parseInt(param.range);
                        obj[3].value = parseInt(param.range);
                        break
                    case "threshold":
                        obj[4].value = parseInt(param.threshold);
                        obj[5].value = parseInt(param.threshold);
                        break
                    case "weight":
                        obj[6].value = parseInt(param.weight);
                        obj[7].value = parseInt(param.weight);
                        break
                    default:
                        break
                }
            }
        } else {
            console.log("SCAN_PARAM : default");
        }
    } catch (err) {
        console.log(err);
    }
};
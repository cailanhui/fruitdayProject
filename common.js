/**
 * Created by tarena on 18-9-30.
 */
function create_xhr() {
    if(window.XMLHttpRequest){
        return new XMLHttpRequest();
    }else{
        return new ActiveXObject('Microsoft.XMLHTTP')
    }
}
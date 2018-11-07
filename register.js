$(function () {
    //表示手机号是否已经被注册的状态值
    var registerStatus = 0;

    //1.为uphone绑定blur事件
    $('input[name="uphone"]').blur(function () {
        if ($(this).val().trim().length === 0) {
            return;
        }
        //如果文本框内有数据，则发送ajax请求，判断数据是否存在
        $.get(
            '/check_uphone/',
            {'uphone':$(this).val()},
            function (data) {
                $('#uphone-tip').html(data.msg);
                //为registerStatus赋值，以便在提交表单时使用
                registerStatus = data.status
            },
            'json'
        );
    });

    //为regForm表单元素绑定submit事件
    $('#regForm').submit(function () {
        //判断registerStatus的值，决定表单是否提交
        if(registerStatus === 1){
            return false;
        }
    })
});

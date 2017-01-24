/**
* Created by WFJ on 2016/11/28.
*/

var API_URL = "/manage/node/data";

var $table = $('#id-for-manage-article'),
    $alert = $('.alert').hide(),
    $btn_add = $('#btn_add'),
    $btn_update = $('#btn_update'),
    $btn_delete = $('#btn_delete'),
    $add_or_update_modal = $('#add_or_update_modal').modal({show: false}),
    selections = [];

function queryParams(params) {
    return {   //这里的键的名字和控制器的变量名必须一直，这边改动，控制器也需要改成一样的
        limit: params.limit,   //页面大小
        offset: params.offset,  //页码
        order: params.order,
        sort: params.sort,
        start_time: $("#txt_search_start_time").val(),
        end_time: $("#txt_search_end_time").val(),
        node_ip: $("#txt_search_node_ip").val(),
        node_status: $("#txt_search_node_status").val()
    };
}

function nodeManageRefreshTable(){
    $table.bootstrapTable('refresh');
}

// 表格配置以及字段初始化
function initTable() {
    $table.bootstrapTable({
        //height: getHeight(),
        queryParams: queryParams,//传递参数（*）
        columns: [
        [
            {
                field: 'state',
                checkbox: true,
                rowspan: 2,
                align: 'center',
                valign: 'middle'
            },
            {
                title: 'Item ID',
                field: '_id',
                rowspan: 2,
                align: 'left',
                valign: 'middle',
                sortable: true
            }, {
                title: 'Item Detail',
                colspan: 8,
                align: 'center'
            }
        ],
        [
            {
                field: 'node_name',
                title: 'Node Name',
                sortable: true,
                align: 'left'
            }, {
                field: 'node_ip',
                title: 'Node IP',
                sortable: true,
                align: 'left',
                clickToSelect: false,
                formatter: ipFormatter,
                events: operateEvents
            }, {
                field: 'auth',
                title: 'Authentication',
                sortable: false,
                formatter: authenticationFormatter,
                align: 'left'
            }, {
                field: 'node_status',
                title: 'Node Status',
                width: 20,
                sortable: true,
                align: 'center',
                formatter: nodeStatusFormatter,
                editable: false
            },{
                field: 'last_detect_time',
                title: 'Last Detect Time',
                sortable: true,
                align: 'left',
                editable: false,
                formatter: timeFormatter
            },
            {
                field: 'last_detect_log',
                title: 'Last Detect Log',
                sortable: false,
                align: 'center',
                editable: false,
                formatter: lastDetectLogFormatter
            }, {
                field: 'has_binding_task',
                title: 'Has Binding Task',
                sortable: true,
                formatter: hasBindingTaskFormatter,
                align: 'center'
            }, {
                field: 'operate',
                title: 'Operate',
                align: 'center',
                clickToSelect: false,
                editable: false,
                events: operateEvents,
                formatter: nodeOperateFormatter
            }
        ]]

    });
    // sometimes footer render error.
    setTimeout(function () {
        $table.bootstrapTable('resetView');
    }, 200);
    $table.on('check.bs.table uncheck.bs.table ' +
            'check-all.bs.table uncheck-all.bs.table', function () {
        $btn_delete.prop('disabled', !$table.bootstrapTable('getSelections').length);

        // save your data, here just save the current page
        selections = getIdSelections();
        // push or splice the selections if you want to save all data selections
    });

    $table.on('check.bs.table uncheck.bs.table', function () {
        $btn_update.prop('disabled', !$table.bootstrapTable('getSelections').length);
        // save your data, here just save the current page
        selections = getIdSelections();
        // 当选中行数超过1，则禁用修改选项
        if (selections.length > 1){
            $btn_update.prop('disabled', true);
        }
        // push or splice the selections if you want to save all data selections
    });

    $btn_delete.click(function () {
        var ids = getIdSelections();
        if (!deleteItems(ids.join(','))) return;
        $table.bootstrapTable('remove', {
            field: '_id',
            values: ids
        });

        $btn_delete.prop('disabled', true);
    });

    $(window).resize(function () {
        $table.bootstrapTable('resetView', {
            height: getHeight()
        });
    });
}

function getIdSelections() {
    return $.map($table.bootstrapTable('getSelections'), function (row) {
        return row._id;
    });
}

function getRowSelections() {
    return $.map($table.bootstrapTable('getSelections'), function (row) {
        return row;
    })[0];
}

function showNodeControlPage(){
    console.log("test showNodeControlPage");
}

function responseHandler(res) {
    $.each(res.rows, function (i, row) {
        row.state = $.inArray(row._id, selections) !== -1;
    });
    return res;
}

function detailFormatter(index, row) {
    var html = [];
    $.each(row, function (key, value) {
        html.push('<p><b>' + key + ' :</b> ' + value + '</p>');
    });
    return html.join('');
}

function nodeOperateFormatter(value, row, index) {
    return [
        '<a class="update text-warning" href="javascript:void(0)" title="Update">',
        '<i class="glyphicon glyphicon-pencil"></i>',
        '</a>',
        '<a class="remove text-danger" href="javascript:void(0)" title="Remove">',
        '<i class="glyphicon glyphicon-remove"></i>',
        '</a>'
    ].join('');
}

function ipFormatter(value, row, index) {
    return [
        '<a class="detail" href="javascript:void(0)" title="Detail">',
        value,
        '</a>'
    ].join('');
}

function timeFormatter(value, row, index) {
    var last_time;
    if (value){
        last_time = new Date(parseInt(value) * 1000).toLocaleString();
    } else {
        last_time = "--";
    }
    return last_time;
}

// 表格中下载脚本格式化
function lastDetectLogFormatter(value, row, index) {
    if (value){
        return [
            '<span style="cursor: pointer;">',
            '<a class="btn-default" style="text-decoration: none;" onclick="downloadScriptFile(\''+row.last_detect_log+'\');">',
            '<i class="glyphicon glyphicon-download-alt"></i>',
            '&nbsp;Download</a>',
            '</span>'
        ].join(' ');
    } else {
        return "--";
    }
}


// 表格中绑定节点列表格式化
function hasBindingTaskFormatter(value, row, index) {
    var return_html;
    if (Number(value) == 1){
        return_html = '<span style="color: lightseagreen"><i class="glyphicon glyphicon-star"></i></span>'
    } else {
        return_html= '';
    }
    return return_html;
}
function showBindingTaskList(_id){
    // 展示绑定的节点
    console.log("show binding task list by id: ", _id);
}


// 具体的下载函数
function downloadScriptFile(filename){
    $.fileDownload('/download/file?filename='+filename)
    .done(function () { alert('File download a success!'); })
    .fail(function () { alert('File download failed!'); });
}
function nodeStatusFormatter(value, row, index) {
    var return_html = "";
    if (value == 1){
        return_html = '<span style="color: green"><i class="glyphicon glyphicon-ok-sign"></i></span>';
    } else {
        return_html = '<span style="color: red"><i class="glyphicon glyphicon-remove-sign"></i></span>'
    }
    return return_html;
}

// 表格显示字段 权限认证格式化
function authenticationFormatter(value, row, index){
    return [
        '<span>',
        row.auth_user,
        '</span>',
        '<span>/',
        row.auth_passwd,
        '</span>'
    ].join(' ');

}


// 表格中操作事件
window.operateEvents = {
    'click .detail': function (e, value, row, index) {
        $("#terminalCmdInteractiveModal").modal('show');
        init_terminal_module_data(row._id);
        init_terminal(row._id);
    },
    'click .show': function (e, value, row, index) {
        ///get  node/timetask/data?limit=10&offset=0&order=asc&start_time=&end_time=&search_id=a6-ac78-49&is_period_execute=2
        console.log("show time task binded.")
    },
    'click .update': function (e, value, row, index) {
        showAddOrUpdateModal($(this).attr('title'), row);
        $add_or_update_modal.modal('show');
        $("#AddOrUpdateNodeInfoForm").attr("action", "/manage/node/data?_id="+row._id);
    },
    'click .remove': function (e, value, row, index) {
        deleteItems(row._id);
    }
};

// 新窗口打开
function windowOpen(url, target){
　　var a = document.createElement("a");
　　a.setAttribute("href", url);
　　if(target == null){
　　  target = '';
　　}
　　a.setAttribute("target", target);
　　document.body.appendChild(a);
　　if(a.click){
　　  a.click();
　　}else{
    　　try{
        　　var evt = document.createEvent('Event');
        　　a.initEvent('click', true, true);
        　　a.dispatchEvent(evt);
    　　}catch(e){
    　　  window.open(url);
    　　}
　　}
　　document.body.removeChild(a);
}

// 删除条目
function deleteItems(ids){
    bootbox.confirm({
        size: "small",
        onEscape: true,
        backdrop: true,
        message: 'Are you sure ?',
        callback: function(result){
            if(result){
                $.ajax({
                    url: API_URL +'?_id=' + ids,
                    type: 'delete',
                    success: function () {
                        $table.bootstrapTable('refresh');
                        showAlert('Delete item successful!', 'success');
                        return true;
                    },
                    error: function () {
                        showAlert('Delete item error!', 'danger');
                    }
                })
            }
        }
    });
    return false;
}

function getHeight() {
    return $(window).height() - $('h1').outerHeight(true);
}

// 显示 添加或更新对话框
function showAddOrUpdateModal(title, row) {
    row = row || {
        _id: '',
        name: '',
        ip: '',
        auth_user: '',
        auth_passwd: '',
        description: ''
    }; // default row value

    $add_or_update_modal.data('_id', row._id);
    $add_or_update_modal.find('.modal-title').text(title);
    for (var name in row) {
        $add_or_update_modal.find('input[name="' + name + '"]').val(row[name]);
        $add_or_update_modal.find('textarea[name="' + name + '"]').val(row[name]);
    }
}

// 更改条目后的提示信息
function showAlert(title, type) {
    $alert.attr('class', 'alert alert-' + type || 'success')
          .html('<i class="glyphicon glyphicon-check"></i> ' + title).show();
    setTimeout(function () {
        $alert.hide();
    }, 3000);
}

// 按钮事件
$(function () {
    // create event
    $btn_add.click(function () {
        var form = $("#AddOrUpdateNodeInfoForm");
        form.attr("action", "/manage/node/data");
        showAddOrUpdateModal($(this).text());
    });
    $btn_update.click(function () {
        var row = getRowSelections();
        var form = $("#AddOrUpdateNodeInfoForm");
        form.attr("action", "/manage/node/data?_id="+row._id);
        showAddOrUpdateModal($(this).text(), row);
    });

    //$add_or_update_modal.find('.submit').click(function () {
        //$("#AddOrUpdateNodeInfoForm").submit();
        //var row = {};
        //
        //$add_or_update_modal.find('input[name]').each(function () {
        //    row[$(this).attr('name')] = $(this).val();
        //});
        //
        //$.ajax({
        //    url: API_URL + ($add_or_update_modal.data('_id') || ''),
        //    type: $add_or_update_modal.data('_id') ? 'put' : 'post',
        //    contentType: 'application/json',
        //    data: JSON.stringify(row),
        //    success: function () {
        //        $add_or_update_modal.modal('hide');
        //        $table.bootstrapTable('refresh');
        //        showAlert(($add_or_update_modal.data('_id') ? 'Update' : 'Create') + ' item successful!', 'success');
        //    },
        //    error: function () {
        //        $add_or_update_modal.modal('hide');
        //        showAlert(($add_or_update_modal.data('_id') ? 'Update' : 'Create') + ' item error!', 'danger');
        //    }
        //});
    //});


    var scripts = [
        location.search.substring(1) || '/static/js/bootstrap/bootstrap-table/bootstrap-table.min.js',
        '/static/js/bootstrap/bootstrap-table/extensions/bootstrap-table-export.js',
        '/static/js/bootstrap/bootstrap-table/extensions/tableExport.js',
        '/static/js/bootstrap/bootstrap-table/extensions/bootstrap-table-editable.js',
        '/static/js/bootstrap/bootstrap-table/extensions/bootstrap-editable.js'
    ],
    eachSeries = function (arr, iterator, callback) {
        callback = callback || function () {};
        if (!arr.length) {
            return callback();
        }
        var completed = 0;
        var iterate = function () {
            iterator(arr[completed], function (err) {
                if (err) {
                    callback(err);
                    callback = function () {};
                }
                else {
                    completed += 1;
                    if (completed >= arr.length) {
                        callback(null);
                    }
                    else {
                        iterate();
                    }
                }
            });
        };
        iterate();
    };

    eachSeries(scripts, getScript, initTable);
});

function getScript(url, callback) {
    var head = document.getElementsByTagName('head')[0];
    var script = document.createElement('script');
    script.src = url;

    var done = false;
    // Attach handlers for all browsers
    script.onload = script.onreadystatechange = function() {
        if (!done && (!this.readyState ||
                this.readyState == 'loaded' || this.readyState == 'complete')) {
            done = true;
            if (callback)
                callback();

            // Handle memory leak in IE
            script.onload = script.onreadystatechange = null;
        }
    };

    head.appendChild(script);

    // We handle everything using the script element injection
    return undefined;
}


// 表格校验
$(document).ready(function() {
    // 美化查询平台中的单选节点状态
    $("#txt_search_node_status").multiselect();
    // 添加或更新节点时，表格校验
    $('#AddOrUpdateNodeInfoForm').bootstrapValidator({
        message: 'This value is not valid',
        excluded: [':disabled'],
        live: 'enable', //是否实时校验，默认开启
        feedbackIcons: {
            valid: 'glyphicon glyphicon-ok',
            invalid: 'glyphicon glyphicon-remove',
            validating: 'glyphicon glyphicon-refresh'
        },
        fields: {
            node_name: {
                trigger: 'keyup',
                validators: {
                    notEmpty: {
                        message: 'The Node Name is required'
                    },
                    stringLength: {
                        min: 1,
                        max: 30,
                        message: 'The Node Name must be more than 6 and less than 30 characters long'
                    },
                    regexp: {
                        regexp: /^[a-zA-Z]+[\w\s\-\.]+[a-zA-Z0-9_]+$/,
                        message: 'The Node Name can only consist of alphabetical, number, space, dot and underscore, but must be start with alphabetical and end with one of alphabetical, number underscore,'
                    }
                }
            },
            node_ip: {
                trigger: 'keyup',
                validators: {
                    notEmpty: {
                        message: 'The Node IP is required'
                    },
                    ip: {
                        message: 'The IP address is not valid'
                    }
                }
            },
            node_port: {
                trigger: 'keyup',
                validators: {
                    notEmpty: {
                        message: 'The Node Port is required'
                    },
                    digits: {
                        message: 'The Node Port number is not valid'
                    },
                    stringLength: {
                        min: 1,
                        max: 5,
                        message: 'The Node Port must be more than 1 and less than 5 characters long'
                    }
                }
            },
            auth_user: {
                trigger: 'keyup',
                validators: {
                    notEmpty: {
                        message: 'The Authentication Username is required'
                    },
                    stringLength: {
                        min: 1,
                        max: 30,
                        message: 'The Authentication Username must be more than 6 and less than 30 characters long'
                    },
                    regexp: {
                        regexp: /^[a-zA-Z]+[\w\s\-\.]+[a-zA-Z0-9_]+$/,
                        message: 'The Authentication Username can only consist of alphabetical, number, dot and underscore, but must be start with alphabetical and end with one of alphabetical, number underscore,'
                    }
                }
            },
            auth_passwd: {
                trigger: 'keyup',
                validators: {
                    notEmpty: {
                        message: 'The Authentication Password is required'
                    },
                    stringLength: {
                        min: 6,
                        max: 128,
                        message: 'The Authentication Password must be more than 6 and less than 128  characters'
                    },
                    regexp: {
                        regexp: /^[a-zA-Z0-9_=+\-]+$/,
                        message: 'The Authentication Password can only consist of alphabetical, number, underscore, +,-,='
                    }
                }
            }
        }
    }).find('[name="node_ip"]').mask('099.099.099.099');

});


function clearCurrentTime(){
    $("[data-link-field='txt_search_start_time']").children("input").val("");
}
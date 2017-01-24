/**
 * Created by WFJ on 2016/12/1.
 */
var API_URL = "/manage/timetask/data";

var $time_task_table = $('#id-for-manage-timetask'),
    $alert = $('.alert').hide(),
    $btn_task_delete = $('#btn_task_delete'),
    $add_time_task_modal = $('#add_time_task_modal').modal({show: false}),
    selections = [],
    $add_time_task = $('#addTimeTaskForm'),
    $binding_node = $('#bindingNodeForm');


// 设置弹出对话框属性
$(document).ready(function() {
    // 设置上传文件的属性
    $("#upload_file_name").fileinput({
        fileSizeGetter: 1
    });
    // 时间格式化
    $('#first_execute_time')
        .datetimepicker({
            weekStart: 1,
            format: "yyyy-mm-dd HH:ii:ss",
            todayBtn:  true,
            autoclose: true,
            todayHighlight: 1,
            startView: 2,
            forceParse: 0,
            pickerPosition: "bottom-left"
        })

        .on('dp.change dp.show', function(e) {
            // Validate the date when user change it
            $batch_add_time_tasks
            // Get the bootstrapValidator instance
            .data('bootstrapValidator')
            // Mark the field as not validated, so it'll be re-validated when the user change date
            .updateStatus('first_execute_time', 'NOT_VALIDATED', null)
            // Validate the field
            .validateField('first_execute_time');
        });

    // 多选初始化
    $binding_node.find('[name="node_ids"]')
            // 初始化多选
            .multiselect({
                includeSelectAllOption: true,
                selectAllValue: 'select-all-value',
                // Re-validate the multiselect field when it is changed
                onChange: function(element, checked) {
                    $binding_node
                        .data('bootstrapValidator')                 // Get plugin instance
                        .updateStatus('node_ids', 'NOT_VALIDATED')  // Update field status
                        .validateField('node_ids');                 // and re-validate it
                }
            })
            .end();
    $binding_node.find('[name="time_task_ids"]')
            // 初始化多选
            .multiselect({
                includeSelectAllOption: true,
                selectAllValue: 'select-all-value',
                // Re-validate the multiselect field when it is changed
                onChange: function(element, checked) {
                    $binding_node
                        .data('bootstrapValidator')                 // Get plugin instance
                        .updateStatus('time_task_ids', 'NOT_VALIDATED')  // Update field status
                        .validateField('time_task_ids');                 // and re-validate it
                }
            })
            .end();
    // 添加校验
    $binding_node.bootstrapValidator({
        // Exclude only disabled fields
        // The invisible fields set by Bootstrap Multiselect must be validated
        excluded: [':disabled'],
        live: 'enable',
        feedbackIcons: {
            valid: 'glyphicon glyphicon-ok',
            invalid: 'glyphicon glyphicon-remove',
            validating: 'glyphicon glyphicon-refresh'
        },
        fields: {
            node_ids: {
                validators: {
                    callback: {
                        message: 'Please choose more than 1 node you use for binding',
                        callback: function(value, validator) {
                            // Get the selected options
                            var options = validator.getFieldElements('node_ids').val();
                            return (options != null && options.length >= 1);
                        }
                    }
                }
            },
            time_task_ids: {
                validators: {
                    callback: {
                        message: 'Please choose more than 1 task you use for binding',
                        callback: function(value, validator) {
                            // Get the selected options
                            var options = validator.getFieldElements('time_task_ids').val();
                            return (options != null && options.length >= 1);
                        }
                    }
                }
            },
            first_execute_time: {
                validators: {
                    validators: {
                        notEmpty: {
                            message: 'The first execute time is required and cannot be empty'
                        },
                        date: {
                            format: 'yyyy-mm-dd HH:ii:ss'
                        }
                    }
                }
            },
            time_task_period_num: {
                validators: {
                    enabled: false,
                    trigger: 'keyup',
                    validators: {
                        notEmpty: {
                            message: 'The time task period number is required and cannot be empty'
                        },
                        digits: {
                            message: 'The time task period number is not valid'
                        }
                    }
                }
            }
        }
    });


    // toggle开关设置
    $add_time_task.find('[name="is_upload_file"]')
        .bootstrapSwitch({
            size: 'small',
            state: true, //设置初始状态
            onText: "YES",
            offText: "NO",
            // 添加change事件处理
            onSwitchChange: function(event, state) {
                var upload_file_name = $("#upload_file_name");
                var manual_input_cmd = $("#manual_input_cmd");
                if (state){
                    upload_file_name.fileinput('enable');
                    manual_input_cmd.attr('disabled', 'disabled');
                } else {
                    manual_input_cmd.removeAttr('disabled');
                    upload_file_name.fileinput('disable');
                }
            },
            // 初始化
            onInit: function(event, state){


            }
        });
});



function queryParamsTimeTaskTable(params) {
    return {   //这里的键的名字和控制器的变量名必须一直，这边改动，控制器也需要改成一样的
        limit: params.limit,   //页面大小
        offset: params.offset,  //页码
        order: params.order,
        sort: params.sort,
        start_time: $("#txt_search_start_time").val(),
        end_time: $("#txt_search_end_time").val(),
        task_name: $("#txt_search_task_name").val(),
        interpreter: $("#txt_search_interpreter").val()
    };
}

function initTimeTaskTable() {
    $time_task_table.bootstrapTable({
        //height: getHeight(),
        queryParams: queryParamsTimeTaskTable,//传递参数（*）
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
                align: 'center',
                valign: 'middle',
                sortable: true
            }, {
                title: 'Item Detail',
                colspan: 6,
                align: 'center'
            }
        ],
        [
            {
                field: 'task_name',
                title: 'Task Name',
                sortable: true,
                align: 'left'
            },{
                field: 'interpreter',
                title: 'Interpreter',
                sortable: true,
                align: 'left'
            },{
                field: 'download_script_file',
                title: 'Download Script File',
                sortable: false,
                formatter: downloadScriptFileFormatter,
                align: 'center'
            },{
                field: 'has_binding_node',
                title: 'Has Binding Node',
                sortable: true,
                formatter: hasBindingNodeFormatter,
                align: 'center'
            }, {
                field: 'create_time',
                title: 'Create Time',
                sortable: true,
                align: 'left',
                formatter: timeFormatter,
                editable: false
            },{
                field: 'operate',
                title: 'Operate',
                align: 'center',
                clickToSelect: false,
                events: operateEvents,
                formatter: operateFormatter
            }
        ]]

    });
    // sometimes footer render error.
    setTimeout(function () {
        $time_task_table.bootstrapTable('resetView');
    }, 200);
    $time_task_table.on('check.bs.table uncheck.bs.table ' +
            'check-all.bs.table uncheck-all.bs.table', function () {
        $btn_task_delete.prop('disabled', !$time_task_table.bootstrapTable('getSelections').length);
        selections = getIdSelections();
        // push or splice the selections if you want to save all data selections
    });


    $btn_task_delete.click(function () {
        var ids = getIdSelections();
        if (!deleteTaskItems(ids.join(','))) return;
        $time_task_table.bootstrapTable('remove', {
            field: '_id',
            values: ids
        });

        $btn_task_delete.prop('disabled', true);
    });


    $(window).resize(function () {
        $time_task_table.bootstrapTable('resetView', {
            height: getHeight()
        });
    });
}

// 启动表格
$(function () {
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

    eachSeries(scripts, getScript, initTimeTaskTable);
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



// 选中的ID
function getIdSelections() {
    return $.map($time_task_table.bootstrapTable('getSelections'), function (row) {
        return row._id;
    });
}


// 表格中定义的响应句柄
function responseHandler(res) {
    $.each(res.rows, function (i, row) {
        row.state = $.inArray(row._id, selections) !== -1;
    });
    return res;
}

// 表格中小加号点击后内容展现方式定义
function detailFormatter(index, row) {
    var html = [];
    $.each(row, function (key, value) {
        html.push('<p><b>' + key + ' :</b> ' + value + '</p>');
    });
    return html.join('');
}

// 表格中时间格式化
function timeFormatter(value, row, index) {
    var last_time;
    if (value){
        last_time = new Date(parseInt(value) * 1000).toLocaleString();
    } else {
        last_time = "--";
    }
    return last_time;
}

// 表格中绑定节点列表格式化
function hasBindingNodeFormatter(value, row, index) {
    var return_html;
    if (Number(value) == 1){
        return_html = '<span style="color: green"><i class="glyphicon glyphicon-ok-sign"></i></span>'
    } else {
        return_html= '<span style="color: red"><i class="glyphicon glyphicon-remove-sign"></i></span>';
    }
    return return_html;
}
// 展示绑定的节点 -- 废弃，这里不好做连接查询
function showBindingNodeList(_id){
    //_blank  _parent _top _self
    url = "/node/timetask/data?limit=10&offset=0&order=asc&search_id="+_id;
    windowOpen(url, "_self")
}
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

// 表格中下载脚本格式化
function downloadScriptFileFormatter(value, row, index) {
    return [
        '<span style="cursor: pointer;">',
        '<a class="btn-default" style="text-decoration: none;" onclick="downloadScriptFile(\''+row.download_script_file+'\');">',
        '<i class="glyphicon glyphicon-download-alt"></i>',
        '&nbsp;Download</a>',
        '</span>'
    ].join(' ');
}

// 表格中点击下载时，下载文件
// 具体的下载函数
function downloadScriptFile(filename){
    $.fileDownload('/download/file?filename='+filename)
    .done(function () { alert('File download a success!'); })
    .fail(function () { alert('File download failed!'); });
}
// 表格中操作动作格式定义
function operateFormatter(value, row, index) {
    return [
        //'<a class="update text-warning" href="javascript:void(0)" title="Update">',
        //'<i class="glyphicon glyphicon-pencil"></i>',
        //'</a>&nbsp;',
        //'<a class="unbind text-default" href="javascript:void(0)" title="Unbind">',
        //'<i class="glyphicon glyphicon-wrench"></i>',
        //'</a>&nbsp;',
        '<a class="remove text-danger" href="javascript:void(0)" title="Remove">',
        '<i class="glyphicon glyphicon-remove"></i>',
        '</a>'
    ].join('');
}


window.operateEvents = {
    //'click .unbind': function (e, value, row, index) {
    //    clearBindedNodes(row._id);
    //},
    'click .remove': function (e, value, row, index) {
        console.log("click remove, do nothing.");
        deleteTaskItems(row._id);
    }
};





function deleteTaskItems(ids){
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
                        $time_task_table.bootstrapTable('refresh');
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

// 更改条目后的提示信息
function showAlert(title, type) {
    $alert.attr('class', 'alert alert-' + type || 'success')
          .html('<i class="glyphicon glyphicon-check"></i> ' + title).show();
    setTimeout(function () {
        $alert.hide();
    }, 3000);
}

function getHeight() {
    return $(window).height() - $('h1').outerHeight(true);
}

function taskManageRefreshTable(){
    $time_task_table.bootstrapTable('refresh');
}
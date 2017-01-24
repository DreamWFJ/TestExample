/**
* Created by WFJ on 2016/11/28.
*/
var $table = $('#id-for-manage-article'),
    $add = $('#btn_add'),
    $task = $('#btn_task'),
    $remove = $('#btn_delete'),
    selections = [];

function initTable() {
    $table.bootstrapTable({
        url: '/manage/article',         //请求后台的URL（*）
        method: 'post',                      //请求方式（*）
        toolbar: '#toolbar',                //工具按钮用哪个容器
        striped: false,                      //是否显示行间隔色
        cache: false,                       //是否使用缓存，默认为true，所以一般情况下需要设置一下这个属性（*）
        dataField: 'rows',                  //设置数据域的键
        sortable: true,                     //是否启用排序
        sortOrder: "asc",                   //排序方式
//                queryParams: oTableInit.queryParams,//传递参数（*）
        sidePagination: "server",           //分页方式：client客户端分页，server服务端分页（*）

        search: true,                       //是否显示表格搜索，此搜索是客户端搜索，不会进服务端，所以，个人感觉意义不大
        strictSearch: true,
        showColumns: true,                  //是否显示所有的列
        showRefresh: true,                  //是否显示刷新按钮
        showToggle: true,                    //是否显示详细视图和列表视图的切换按钮
        showFooter: false,                   //是否显示汇总行
        showExport: true,                   //是否显示导出

        pagination: true,                   //是否显示分页（*）
        showPaginationSwitch: true,         //是否显示分页按钮

        pageNumber: 1,                       //初始化加载第一页，默认第一页
        pageSize: 10,                       //每页的记录行数（*）
        pageList: [10, 25, 50, 100],        //可供选择的每页的行数（*）



        minimumCountColumns: 2,             //最少允许的列数
        clickToSelect: true,                //是否启用点击选中行
        uniqueId: "_id",                     //每一行的唯一标识，一般为主键列
        idField: "_id",
        cardView: false,                    //是否显示详细视图
        detailView: true,                   //是否显示父子表，查看详细信息
        detailFormatter: detailFormatter,   //详细信息具体展示方式
        responseHandler: responseHandler,   //远程数据加载之前,处理程序响应数据格式,对象包含的参数:res:响应数据。

//                height: getHeight(), //行高，如果没有设置height属性，表格自动根据记录条数觉得表格高度
//                paginationFirstText: 'First',
        paginationPreText: 'Previous',
        paginationNextText: 'Next',
//                paginationLastText: 'Last',
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
                field: 'name',
                title: 'Node Name',
                sortable: true,
                align: 'left'
            }, {
                field: 'ip',
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
                align: 'left'
            }, {
                field: 'node_status',
                title: 'Node Status',
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
            },{
                field: 'operate',
                title: 'Operate',
                align: 'center',
                events: operateEvents,
                formatter: operateFormatter
            }
        ]]

    });
    // sometimes footer render error.
    setTimeout(function () {
        $table.bootstrapTable('resetView');
    }, 200);
    $table.on('check.bs.table uncheck.bs.table ' +
            'check-all.bs.table uncheck-all.bs.table', function () {
        $remove.prop('disabled', !$table.bootstrapTable('getSelections').length);
        $task.prop('disabled', !$table.bootstrapTable('getSelections').length);

        // save your data, here just save the current page
        selections = getIdSelections();
        // push or splice the selections if you want to save all data selections
    });
    $table.on('expand-row.bs.table', function (e, index, row, $detail) {
        if (index % 2 == 1) {
            $detail.html('Loading from ajax request...');
            $.get('LICENSE', function (res) {
                $detail.html(res.replace(/\n/g, '<br>'));
            });
        }
    });
//            $table.on('all.bs.table', function (e, name, args) {
//                console.log(name, args);
//            });
    $remove.click(function () {
        var ids = getIdSelections();
        $table.bootstrapTable('remove', {
            field: 'id',
            values: ids
        });
        $remove.prop('disabled', true);
    });
    $task.click(function () {
        var ids = getIdSelections();

        $task.prop('disabled', true);
    });
    $(window).resize(function () {
        $table.bootstrapTable('resetView', {
            height: getHeight()
        });
    });
}

function getIdSelections() {
    return $.map($table.bootstrapTable('getSelections'), function (row) {
        return row.id
    });
}

function showNodeControlPage(){
    console.log("test showNodeControlPage");
}
function responseHandler(res) {
    $.each(res.rows, function (i, row) {
        row.state = $.inArray(row.id, selections) !== -1;
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

function operateFormatter(value, row, index) {
    return [
        '<a class="task" href="javascript:void(0)" title="Time Task">',
        '<i class="glyphicon glyphicon-tasks"></i>',
        '</a>  ',
        '<a class="edit text-info" href="javascript:void(0)" title="Edit">',
        '<i class="glyphicon glyphicon-pencil"></i>',
        '</a>  ',
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
    return new Date(parseInt(value) * 1000).toLocaleString();
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

window.operateEvents = {
    'click .detail': function (e, value, row, index) {
        console.log('link detail information');
    },
    'click .edit': function (e, value, row, index) {
        console.log('You click edit action');
    },
    'click .task': function (e, value, row, index) {
        alert('You click task action, row: ' + JSON.stringify(row));
    },
    'click .remove': function (e, value, row, index) {
        $table.bootstrapTable('remove', {
            field: 'id',
            values: [row.id]
        });
    }
};

function totalNameFormatter(data) {
    return data.length;
}

function totalPriceFormatter(data) {
    var total = 0;
    $.each(data, function (i, row) {
        total += +(row.price.substring(1));
    });
    return '$' + total;
}

function getHeight() {
    return $(window).height() - $('h1').outerHeight(true);
}

$(function () {
    var scripts = [
            location.search.substring(1) || '/static/js/bootstrap-table/bootstrap-table.min.js',
            '/static/js/bootstrap-table/extensions/bootstrap-table-export.js',
            '/static/js/bootstrap-table/extensions/tableExport.js',
            '/static/js/bootstrap-table/extensions/bootstrap-table-editable.js',
            '/static/js/bootstrap-table/extensions/bootstrap-editable.js'
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
/**
 * @Description: 上传提交
 * @date 2024/1/17
 */
function uploadFile() {
    const fileInput = document.getElementById('fileInput');
    let { pathname } = window.location;

    fileInput.addEventListener('change', (e) => {
        const files = e.target;

        const xhr = new XMLHttpRequest();
        // xhr.open('POST', `/upload?file_path=${pathname.substr(1)}`, true);
        xhr.open('POST', pathname, true);
        xhr.onreadystatechange = function () {
            if (xhr.readyState === 4 && xhr.status === 200) {
                alert('上传成功');
                // 自动刷新
                window.location.reload();
            }
        };

        const formData = new FormData();
        for (let i = 0; i < files.files.length; i++) {
            formData.append('files', files.files[i]);
        }
        // formData.append('file', file);
        xhr.send(formData);
    })
}


// 引入fetch API或者使用XMLHttpRequest等其他方式发起HTTP请求
async function postData(url = '', data = {}) {
    const response = await fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json', // 根据实际情况调整Content-Type
        },
        body: JSON.stringify(data),
    });
    return response.json(); // 假设后端返回JSON格式数据
}

async function putData(url = '', data = {}) {
    const response = await fetch(url, {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json', // 根据实际情况调整Content-Type
        },
        body: JSON.stringify(data),
    });
    return response.json(); // 假设后端返回JSON格式数据
}


// 创建文件夹按钮点击事件监听
function mkdir(){
    document.getElementById('createFolder').addEventListener('click', async function() {
        const folderName = prompt('请输入要创建的文件夹名称：');
        let { pathname } = window.location;
        if (folderName && folderName.trim() !== '') {
            try {
                const response = await postData(`/mkdir?file_path=${pathname.substr(1)}&dirname=${folderName}`, );
                console.log('文件夹创建成功:', response);
                // 自动刷新
                window.location.reload();
            } catch (error) {
                console.error('文件夹创建失败:', error);
            }
        } else {
            alert('请输入有效的文件夹名称');
        }
    });
}

function mkdir2(){
    document.getElementById('createFolder').addEventListener('click', async function() {
        const folderName = prompt('请输入要创建的文件夹名称：');
        let { pathname } = window.location;
        if (folderName && folderName.trim() !== '') {
            try {
                let curPath = pathname.substring(1)
                console.log('curPath:', curPath)
                // let mkdirUrl = folderName ? curPath === '' : curPath + '/' + folderName
                // const response = await putData(mkdirUrl,);
                const response = await putData(curPath+"?dir_name="+folderName,);
                console.log('文件夹创建成功:', response);
                // 自动刷新
                window.location.reload();
            } catch (error) {
                console.error('文件夹创建失败:', error);
            }
        } else {
            alert('请输入有效的文件夹名称');
        }
    });
}

function back(){
    document.getElementById('backButton').addEventListener('click', function (){
        history.back();
    });
}


/**
 * @Description: 加载完成后执行
 * @date 2024/1/17
 */
window.onload = () => {
    uploadFile()
    mkdir2()
    back()
}
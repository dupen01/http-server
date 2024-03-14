import os
import time

import uvicorn
import secrets
from fastapi import FastAPI, Request, HTTPException, UploadFile, Form, Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi.responses import HTMLResponse, FileResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

app = FastAPI()

security = HTTPBasic()


def get_current_user(credentials: HTTPBasicCredentials = Depends(security)):
    current_username = credentials.username.encode('utf8')
    current_password = credentials.password.encode('utf8')
    if os.environ.get('HTTP_USER') and os.environ.get('HTTP_PASSWORD'):
        correct_username = os.environ.get('HTTP_USER').encode('utf8')
        correct_password = os.environ.get('HTTP_PASSWORD').encode('utf8')
        is_correct_username = secrets.compare_digest(current_username, correct_username)
        is_correct_password = secrets.compare_digest(current_password, correct_password)
        if not (is_correct_username and is_correct_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Basic"}
            )
    return credentials.username


script_dir = os.path.dirname(__file__)
st_abs_path = os.path.join(script_dir, "static/")
tplt_abs_path = os.path.join(script_dir, "templates/")
app.mount("/static", StaticFiles(directory=st_abs_path), name="static")
templates = Jinja2Templates(directory=tplt_abs_path)


class FileInfo:
    def __init__(self, name, mtime, size, ftype):
        self.name = name
        self.mtime = mtime
        self.size = size
        self.ftype = ftype


class FileReader:
    def __init__(self, work_dir="."):
        self.work_dir = work_dir

    def get_files(self, file_path):
        files = []
        fullname = os.path.join(self.work_dir, file_path)
        if os.path.isdir(fullname):
            for name in sorted(os.listdir(fullname), key=lambda x: x.lower()):
                child_fullname = os.path.join(fullname, name)
                file_type = '文件夹'
                file_size = '--'
                _time = time.strftime("%Y年%m月%d日 %H:%M", time.localtime(os.path.getmtime(child_fullname)))
                if os.path.isfile(child_fullname):
                    file_size = self.__get_file_size(child_fullname)
                    file_type = os.path.splitext(child_fullname)[1][1:]
                if not (name.startswith('.') or name.startswith('__')):
                    files.append(FileInfo(name, _time, file_size, file_type))
        files.sort(key=lambda x: x.mtime, reverse=True)
        return files

    @staticmethod
    def __get_file_size(file_name):
        size = os.path.getsize(file_name)
        if size < 1024:
            return f"{size} 字节"
        elif 1024 <= size < 1024 * 1024:
            return f"{round(size / 1024, 2)} KB"
        elif 1024 <= size < 1024 * 1024 * 1024:
            return f"{round(size / (1024 * 1024), 2)} MB"
        else:
            return f"{round(size / (1024 * 1024 * 1024), 2)} GB"


@app.post("/{file_path:path}")
async def upload_file(file_path, files: list[UploadFile]):
    for file in files:
        full_path = os.path.join(file_path, file.filename)
        with open(full_path, 'wb') as f:
            f.write(file.file.read())
    return {
        "msg": "upload succeed"
    }


@app.put("/{file_path:path}")
def mkdir(file_path, dir_name):
    dir_path = os.path.join(file_path, dir_name)
    os.makedirs(dir_path)
    return {
        "msg": f"directory {dir_path} created",
    }


@app.delete('/{file_path:path}')
def delete(file_path):
    if os.path.isfile(file_path):
        os.remove(file_path)
    else:
        import shutil
        shutil.rmtree(file_path)
    return {
        "msg": f"file or directory {file_path} deleted"
    }


@app.get("/{file_path:path}")
def read_file(request: Request, file_path, username: str = Depends(get_current_user)):
    fr = FileReader()
    result = fr.get_files(file_path)
    request_url = request.url
    if file_path == "":
        file_path = "."
    if not str(request.url).endswith('/'):
        request_url = str(request.url) + '/'
    if os.path.exists(file_path):
        if os.path.isdir(file_path):
            return templates.TemplateResponse("index.html",
                                              {"request": request,
                                               "file_path": '' if file_path == '.' else file_path,
                                               "result": result,
                                               "request_url": request_url
                                               })
        else:
            if file_path.endswith('.xml'):
                return FileResponse(file_path, media_type='text/plain')
            return FileResponse(file_path)
    else:
        return templates.TemplateResponse("error.html",
                                          {"request": request,
                                           })


if __name__ == '__main__':
    # os.environ.setdefault("HTTP_USER", "tt")
    # os.environ.setdefault("HTTP_PASSWORD", "tt123")
    uvicorn.run("http_server:app", host='0.0.0.0', port=8080, reload=True)

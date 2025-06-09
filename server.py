from flask import Flask, request, send_file, render_template
from PIL import Image
import numpy as np
from stl import mesh
import io, tempfile, os, traceback

app = Flask(__name__)

dirs = [(-1, -1),  # 左上
        (-1,  0),  # 上
        (-1,  1),  # 右上
        ( 0,  1),  # 右
        ( 1,  1),  # 右下
        ( 1,  0),  # 下
        ( 1, -1),  # 左下
        ( 0, -1)]  # 左

def extract_boundary(mask):
    h, w = mask.shape
    boundary = np.zeros_like(mask, dtype=np.uint8)
    for y in range(h):
        for x in range(w):
            if mask[y, x] == 0:
                continue
            for dy, dx in dirs:
                ny, nx = y + dy, x + dx
                if (0 <= ny < h and 0 <= nx < w) and mask[ny, nx] == 0:
                    boundary[y, x] = 1
    return boundary

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    try:
        # 1. 入力画像読み込み & サイズ調整
        img_base   = Image.open(request.files['base']).convert('RGBA')
        img_target = Image.open(request.files['target']).convert('RGBA')
        w, h = img_base.size
        img_target = img_target.resize((w, h))

        # 2. グレースケール化 & アルファチャンネル取得
        gray_base   = np.array(img_base.convert('L'), dtype=np.float32)
        gray_target = np.array(img_target.convert('L'), dtype=np.float32)
        alpha       = np.array(img_target.split()[3], dtype=np.uint8)

        # 3. パラメータ
        depth     = float(request.form.get('scale', 1.0))
        thickness = float(request.form.get('thickness', 1.0))
        top_z     = 0.0

        # 4. 高さマップとマスク生成
        mask = (gray_target != gray_base) & (alpha > 0)
        height_map = np.where(mask, top_z - depth, top_z)

        # 5. 表面メッシュ生成
        verts, faces = [], []
        for y in range(h-1):
            for x in range(w-1):
                if alpha[y, x] and alpha[y, x+1] and alpha[y+1, x] and alpha[y+1, x+1]:
                    z00 = height_map[y,   x]
                    z10 = height_map[y,   x+1]
                    z01 = height_map[y+1, x]
                    z11 = height_map[y+1, x+1]
                    idx = len(verts)
                    verts += [(x,   y,   z00), (x+1, y,   z10),
                              (x,   y+1, z01), (x+1, y+1, z11)]
                    faces += [[idx, idx+2, idx+1], [idx+1, idx+2, idx+3]]

        # 6. 底面メッシュ生成
        bottom_z = -thickness
        for y in range(h-1):
            for x in range(w-1):
                if alpha[y, x] and alpha[y, x+1] and alpha[y+1, x] and alpha[y+1, x+1]:
                    idx = len(verts)
                    verts += [(x,   y,   bottom_z), (x+1, y,   bottom_z),
                              (x,   y+1, bottom_z), (x+1, y+1, bottom_z)]
                    faces += [[idx, idx+1, idx+2], [idx+1, idx+3, idx+2]]

        # 7. 側面メッシュ生成（境界抽出＋4方向ループ）
        boundary = extract_boundary(alpha.astype(np.uint8))
        # 方向ベクトルのみ定義
        dirs = [( 0,  1), ( 0, -1), ( 1,  0), (-1,  0)]

        for y in range(h):
            for x in range(w):
                if boundary[y, x] != 1:
                    continue
                z00 = height_map[y, x]
                zb0 = bottom_z
                sum = 0
                for dy, dx in dirs:
                    ny, nx = y + dy, x + dx
                    # 背景や画像外なら側面を張る
                    if (0 <= ny < h and 0 <= nx < w) and boundary[ny, nx] == 1:
                        # 隣接セル位置の高さ（存在しなければ z00）
                        sum += 1
                        z01 = height_map[ny, nx] if (0 <= ny < h and 0 <= nx < w) else z00
                        zb1 = bottom_z
                        idx = len(verts)
                        verts += [
                            (x ,   y ,   0),  # v0
                            (nx,   ny,   -thickness),  # v1
                            (nx ,   ny ,   0),  # v2
                            (x,   y,   -thickness)   # v3
                        ]
                        faces += [[idx, idx+2, idx+1], [idx+1, idx+2, idx+3]]

        # 8. STL モデル生成 & 返却
        verts_np = np.array(verts)
        faces_np = np.array(faces)
        model = mesh.Mesh(np.zeros(len(faces_np), dtype=mesh.Mesh.dtype))
        for i, f in enumerate(faces_np):
            model.vectors[i] = verts_np[f]

        with tempfile.NamedTemporaryFile(suffix='.stl', delete=False) as tmp:
            model.save(tmp.name)
            tmp_path = tmp.name
        data = open(tmp_path, 'rb').read()
        os.remove(tmp_path)
        return send_file(
            io.BytesIO(data),
            as_attachment=True,
            download_name='3dcard.stl',
            mimetype='application/vnd.ms-pki.stl'
        )
    except Exception as e:
        app.logger.error(traceback.format_exc())
        return f"Server Error: {e}", 500

if __name__ == '__main__':
    app.run(debug=True)
# ♟️ Chess AI with Pygame GUI
## 🔍 Search Engine
- **Iterative Deepening**
- **Alpha-Beta Pruning**
- **Quiescence Search**
- **Null Move Pruning**
### Transposition Table
- Lưu trữ các thế cờ đã được đánh giá
- Sử dụng **Zobrist Hashing** để mã hóa trạng thái bàn cờ
- Ba loại đánh dấu: `EXACT`, `LOWER`, `UPPER`
### Move Ordering
- **MVV-LVA** (Most Valuable Victim - Least Valuable Attacker)
- **Killer Moves**
- **History Heuristic**
- **SEE (Static Exchange Evaluation)
- **TT Move Boost**
#### 🧮 Evaluation Function
- **Material Counting**
- **Piece-Square Tables**
- **Endgame Scaling**
##### 📖 Opening Book 
- Sử dụng **Opening Book** dưới định dạng **Polyglot (`.bin`)**
###### ▶️ Cách chạy
- pip install pygame python-chess
- python main.py
### Thành quả đạt được 
- Đánh thắng con bot trên web chess.com với elo 2200.
### Đóng góp 
- Lê Ngọc Quý 33,33%
- Trần Văn Đông 33,33%
- Nguyễn Quang Bảo Sơn 33,33%
### Link demo 
https://www.youtube.com/watch?v=SsOv2X2SAXg&t=7s
📚 Nguồn tham khảo
https://www.youtube.com/watch?v=U4ogK0MIzqk&t=1045s

var winWidth = 700; //キャンバス横幅
var winHeight = 600; //キャンバス縦幅
var len = 40; //結合長
var symbolList1 = ["C","O","H","N","S"];

var display = document.getElementById("show");
var c1 = document.getElementById("canvas1");
var base = c1.getContext("2d");
var c2 = document.getElementById("canvas2");
var main = c2.getContext("2d");
var c3 = document.getElementById("canvas3");
var eff1 = c3.getContext("2d");
var c4 = document.getElementById("canvas4");
var eff2 = c4.getContext("2d");

var downX, downY, moveX, moveY, upX, upY;
var downFlag = 0;//0:デフォルト 1:原子 2:結合 3:空
var downId = 999;
var moveFlag = 0;//0:デフォルト 1:原子 2:結合
var moveId = 999;
var demiAngle = 1;
var atomSym;

window.onload = function () {
    background();
    setButton();
};

c4.onmousedown = function (down) {
    downX = down.offsetX;
    downY = down.offsetY;
    //キャンバス内
    if (60 <= downX && downX <= 670 && 30 <= downY && downY <= 570) {
        if (status == 0) {
            switch (moveFlag) {
                case 0:
                    downFlag = 3;
                    ring(downX, downY);
                    return;
                case 1:
                    downFlag = 1;
                    downId = moveId;
                    ring(atoms[downId][1], atoms[downId][2]);
                    return;
                case 2:
                    downFlag = 2;
                    downId = moveId;
                    return;
            }
        } else if (status == 1) {
            switch (moveFlag) {
                case 0:
                    return;
                case 1:
                    var deleteBond = listUpSideBond(moveId);
                    console.log("delete atom", moveId, "in 56");
                    atoms.splice(moveId, 1);
                    refreshId(0);
                    for (var i = 0, l = deleteBond.length; i < l; i++) {
                        bonds.splice(deleteBond[l-i-1], 1);
                    }
                    refreshId(1);
                    redraw();
                    return;
                case 2:
                    bonds.splice(moveId, 1);
                    refreshId(1);
                    redraw();
                    return;
            }
        } else if(status==2){
            atomSym = inAtomList(downX,downY);
            if(atomSym==void 0){
                return;
            }else{
                display.innerHTML = atomSym;
                clear(eff2);
                status = 3;
                return;
            }
        } else if(status==3){
            if(moveFlag==1){
                atoms[moveId][3] = atomSym;
                setAtom(atoms[moveId][1],atoms[moveId][2]);
            }
            return;
        }
    } else {
        //キャンバス外
        if (0 <= downX && downX <= 50 && 50 <= downY && downY <= 100) {
            status = 0;
            display.innerHTML = "デフォルト";
        } else if (0 <= downX && downX <= 50 && 110 <= downY && downY <= 160) {
            if(status==2){
                clear(eff2);
                status = 0;
                display.innerHTML = "デフォルト";
                return;
            }
            status = 2;
            showAtomList();
            display.innerHTML ="原子";
        } else if (0 <= downX && downX <= 50 && 170 <= downY && downY <= 220) {
            status = 1;
            display.innerHTML ="削除";
        } else if (0 <= downX && downX <= 50 && 230 <= downY && downY <= 280) {
            downFlag = 0;
            downId = 999;
            moveFlag = 0;
            moveId = 999;
            demiAngle = 1;
            clear(main);
            clear(eff1);
            clear(eff2);
            atoms = [];
            bonds = [];
            status = 0;
            display.innerHTML = "デフォルト";
        }
    }
};
c4.onmousemove = function (move) {
    moveX = move.offsetX;
    moveY = move.offsetY;
    if(status==2){
        return;
    }
    var atom = atoms.find(function (nowAtom) {
        return inRound(moveX, moveY, nowAtom[1], nowAtom[2]);
    });
    if (atom !== void 0) {
        demiAngle = 1;
        if (moveFlag != 1 || moveId != atom[0]) {
            clear(eff1);
            clear(eff2);
            moveFlag = 1;
            moveId = atom[0];
            atomMark(atom[0]);
            if (downFlag == 1) {
                if (downId != moveId) {
                    ring(atoms[downId][1], atoms[downId][2]);
                    demiBond(downId, moveId);
                }
            } else if (downFlag == 3) {
                ring(downX, downY);
                demiBond2(downX, downY, moveId);
            }
        }
        return;
    }
    if (downFlag == 1) {
        if (moveFlag == 1) {
            clear(eff1);
            clear(eff2);
        }
        moveFlag = 0;
        var ang = direction(moveX, moveY, atoms[downId][1], atoms[downId][2]);
        if (ang == demiAngle) {
            return;
        } else {
            clear(eff2);
            clear(eff1);
            ring(atoms[downId][1], atoms[downId][2]);
            demiAngle = ang;
            radLine(atoms[downId][1], atoms[downId][2], demiAngle, 0);
            return;
        }
    } else if (downFlag == 3) {
        moveFlag = 0;
        var aang = direction(moveX, moveY, downX, downY);
        if (aang == demiAngle) {
            return;
        } else {
            clear(eff1);
            clear(eff2);
            ring(downX, downY);
            demiAngle = aang;
            radLine(downX, downY, demiAngle, 0);
            return;
        }
    }
    var bond = bonds.find(function (nowBond) {
        return inRound(moveX, moveY, nowBond[1], nowBond[2]);
    });
    if (bond !== void 0) {
        if (moveFlag != 2 || moveId != bond[0]) {
            clear(eff1);
            clear(eff2);
            moveFlag = 2;
            moveId = bond[0];
            bondMark(bond[0]);
        }
        return;
    }
    clear(eff1);
    moveFlag = 0;
};
c4.onmouseup = function (up) {
    if(status==2||status==3){
        return;
    }
    clear(eff1);
    clear(eff2);
    upX = up.offsetX;
    upY = up.offsetY;
    switch (downFlag) {
        case 0:
            break;
        case 1:
            switch (moveFlag) {
                case 0:
                    radLine(atoms[downId][1], atoms[downId][2], demiAngle, 1);
                    break;
                case 1:
                    if (downId != moveId) {
                        newBond(downId, moveId);
                    } else {
                        atomMark(downId);
                    }
                    break;
                case 2:
                    break;
            }
            break;
        case 2:
            if (moveFlag == 2) {
                if (downId == moveId) {
                    switch (bonds[downId][5]) {
                        case 1:
                            drawDoubleBond(downId);
                            changeBond(downId, 2);
                            break;
                        case 2:
                            drawTripleBond(downId);
                            changeBond(downId, 3);
                            break;
                        case 3:
                            break;
                    }
                    bondMark(moveId);
                }
            }
            break;
        case 3:
            switch (moveFlag) {
                case 0:
                    radLine(downX, downY, demiAngle, 2);
                    break;
                case 1:
                    var a = newAtom(downX, downY, "C");
                    newBond(a, moveId);
                    break;
                case 2:
                    break;
            }
            break;
    }
    downFlag = 0;
    downId = 999;
    demiAngle = 1;
};

function background() {
    base.fillStyle = "rgb(255,255,255)";
    base.fillRect(60, 30, 610, 540);
}
function setButton() {
    var img1 = new Image(50,50);
    img1.src = "images/bond_icon.png";
    img1.onload = function(){
        base.drawImage(img1,0,50);
    };
    var img2 = new Image(50,50);
    img2.src = "images/hetero_icon.png";
    img2.onload = function(){
        base.drawImage(img2,0,110);
    };
    var img3 = new Image(50,50);
    img3.src = "images/eraser_icon.png";
    img3.onload = function(){
        base.drawImage(img3,0,170);
    };
    var img4 = new Image(50,50);
    img4.src = "images/delete_icon.png";
    img4.onload = function(){
        base.drawImage(img4,0,230);
    };
}
function newAtom(x, y, symbol) {
    var q = atoms.length;
    atoms.push([q, x, y, symbol]);
    return q;
}
function newBond(a, b) {
    var q = bonds.length;
    var x = (atoms[a][1] + atoms[b][1]) / 2;
    var y = (atoms[a][2] + atoms[b][2]) / 2;
    main.beginPath();
    main.lineWidth = 1;
    main.moveTo(atoms[a][1], atoms[a][2]);
    main.lineTo(atoms[b][1], atoms[b][2]);
    main.stroke();
    bonds.push([q, x, y, a, b, 1]);
}
function drawBond(ax, ay, bx, by) {
    main.beginPath();
    main.lineWidth = 1;
    main.moveTo(ax, ay);
    main.lineTo(bx, by);
    main.stroke();
}
function changeBond(bondId, type) {
    var oldBond = bonds[bondId];
    bonds[bondId] = [oldBond[0], oldBond[1], oldBond[2], oldBond[3], oldBond[4], type];
}
function demiBond(a, b) {
    eff2.beginPath();
    eff2.lineWidth = 2;
    eff2.strokeStyle = "rgba(0,255,255,0.5)";
    eff2.moveTo(atoms[a][1], atoms[a][2]);
    eff2.lineTo(atoms[b][1], atoms[b][2]);
    eff2.stroke();
}
function demiBond2(x, y, b) {
    eff2.beginPath();
    eff2.lineWidth = 2;
    eff2.strokeStyle = "rgba(0,255,255,0.5)";
    eff2.moveTo(x, y);
    eff2.lineTo(atoms[b][1], atoms[b][2]);
    eff2.stroke();
}
function clear(layer) {
    layer.clearRect(0, 0, winWidth, winHeight);
}
function atomMark(id) {
    eff1.beginPath();
    eff1.fillStyle = "rgba(0,0,255,0.5)";
    eff1.arc(atoms[id][1], atoms[id][2], len / 5, 0, Math.PI * 2, true);
    eff1.fill();
}
function bondMark(id) {
    eff1.beginPath();
    eff1.fillStyle = "rgba(0,255,0,0.5)";
    eff1.arc(bonds[id][1], bonds[id][2], len / 5, 0, Math.PI * 2, true);
    eff1.fill();
}
function ring(x, y) {
    eff1.beginPath();
    eff1.strokeStyle = "rgba(0,0,255,0.5)";
    eff1.arc(x, y, len * 3 / 10, 0, Math.PI * 2, true);
    eff1.stroke();
}
function inRound(nowX, nowY, targetX, targetY) {
    if (Math.pow(targetX - nowX, 2) + Math.pow(targetY - nowY, 2) <= Math.pow(len / 4, 2)) {
        return true;
    } else {
        return false;
    }
}
function getAngle(nowX, nowY, targetX, targetY) {
    //戻り値:0~2π
    if (nowY - targetY == 0) {
        if (nowX - targetX >= 0) {
            return Math.PI / 2;
        } else {
            return 3 * Math.PI / 2;
        }
    }
    var angle = Math.atan((nowX - targetX) / -(nowY - targetY));
    if ((nowY - targetY) > 0) {
        angle += Math.PI;
    }
    if (angle <= 0) {
        angle += Math.PI * 2;
    }
    return angle;
}
function direction(nowX, nowY, targetX, targetY) {
    if (nowY - targetY == 0) {
        if (nowX - targetX >= 0) {
            return Math.PI / 2;
        } else {
            return -Math.PI / 2;
        }
    }
    var angle = Math.atan((nowX - targetX) / -(nowY - targetY));
    if ((nowY - targetY) > 0) {
        angle += Math.PI;
    }
    if (-Math.PI * 5 / 12 <= angle && angle < -Math.PI / 4) {
        angle = -Math.PI / 3;
    } else if (-Math.PI / 4 <= angle && angle < -Math.PI / 12) {
        angle = -Math.PI / 6;
    } else if (-Math.PI / 12 <= angle && angle < Math.PI / 12) {
        angle = 0;
    } else if (Math.PI / 12 <= angle && angle < Math.PI / 4) {
        angle = Math.PI / 6;
    } else if (Math.PI / 4 <= angle && angle < Math.PI * 5 / 12) {
        angle = Math.PI / 3;
    } else if (Math.PI * 5 / 12 <= angle && angle < Math.PI * 7 / 12) {
        angle = Math.PI / 2;
    } else if (Math.PI * 7 / 12 <= angle && angle < Math.PI * 3 / 4) {
        angle = Math.PI * 2 / 3;
    } else if (Math.PI * 3 / 4 <= angle && angle < Math.PI * 11 / 12) {
        angle = Math.PI * 5 / 6;
    } else if (Math.PI * 11 / 12 <= angle && angle < Math.PI * 13 / 12) {
        angle = Math.PI;
    } else if (Math.PI * 13 / 12 <= angle && angle < Math.PI * 5 / 4) {
        angle = Math.PI * 7 / 6;
    } else if (Math.PI * 5 / 4 <= angle && angle < Math.PI * 17 / 12) {
        angle = Math.PI * 4 / 3;
    } else {
        angle = -Math.PI / 2;
    }
    return angle;
}
function radLine(x, y, angle, pattern) {
    var newX = x + len * Math.sin(angle);
    var newY = y - len * Math.cos(angle);
    switch (pattern) {
        case 0:
            eff2.beginPath();
            eff2.lineWidth = 2;
            eff2.strokeStyle = "rgba(0,255,255,0.5)";
            eff2.moveTo(x, y);
            eff2.lineTo(newX, newY);
            eff2.stroke();
            break;
        case 1:
            var c = newAtom(newX, newY, "C");
            newBond(downId, c);
            break;
        case 2:
            var a = newAtom(x, y, "C");
            var b = newAtom(newX, newY, "C");
            newBond(a, b);
            break;
    }
}
function doubleSide(a, b, c) {
    //a-b-cの結合があり、a-bが2重結合となる
    var baAngle = getAngle(atoms[b][1], atoms[b][2], atoms[a][1], atoms[a][2]);
    var bx, by, ax, ay;
    if (c === void 0) {
        bx = atoms[b][1] + len / 5 * Math.sin(baAngle - 3 * Math.PI / 4);
        by = atoms[b][2] - len / 5 * Math.cos(baAngle - 3 * Math.PI / 4);
        ax = atoms[a][1] + len / 5 * Math.sin(baAngle - Math.PI / 4);
        ay = atoms[a][2] - len / 5 * Math.cos(baAngle - Math.PI / 4);
    } else {
        var bcAngle = getAngle(atoms[b][1], atoms[b][2], atoms[c][1], atoms[c][2]);
        var angle = baAngle - bcAngle;
        if ((-2 * Math.PI <= angle && angle < -Math.PI) || (0 <= angle && angle < Math.PI)) {
            bx = atoms[b][1] + len / 5 * Math.sin(baAngle + 3 * Math.PI / 4);
            by = atoms[b][2] - len / 5 * Math.cos(baAngle + 3 * Math.PI / 4);
            ax = atoms[a][1] + len / 5 * Math.sin(baAngle + Math.PI / 4);
            ay = atoms[a][2] - len / 5 * Math.cos(baAngle + Math.PI / 4);
        } else {
            bx = atoms[b][1] + len / 5 * Math.sin(baAngle - 3 * Math.PI / 4);
            by = atoms[b][2] - len / 5 * Math.cos(baAngle - 3 * Math.PI / 4);
            ax = atoms[a][1] + len / 5 * Math.sin(baAngle - Math.PI / 4);
            ay = atoms[a][2] - len / 5 * Math.cos(baAngle - Math.PI / 4);
        }
    }
    return [bx, by, ax, ay];
}
function searchSideBond(downBondId, nowBondId) {
    if (downBondId == nowBondId) {
        return false;
    } else if (bonds[downBondId][3] == bonds[nowBondId][3]) {
        return true;
    } else if (bonds[downBondId][3] == bonds[nowBondId][4]) {
        return true;
    } else if (bonds[downBondId][4] == bonds[nowBondId][3]) {
        return true;
    } else if (bonds[downBondId][4] == bonds[nowBondId][4]) {
        return true;
    } else {
        return false;
    }
}
function lineUpABC(mainBondId, sideBondId) {
    var a, b, c;
    if (bonds[mainBondId][3] == bonds[sideBondId][3]) {
        a = bonds[mainBondId][4];
        b = bonds[mainBondId][3];
        c = bonds[sideBondId][4];
    } else if (bonds[mainBondId][3] == bonds[sideBondId][4]) {
        a = bonds[mainBondId][4];
        b = bonds[mainBondId][3];
        c = bonds[sideBondId][3];
    } else if (bonds[mainBondId][4] == bonds[sideBondId][3]) {
        a = bonds[mainBondId][3];
        b = bonds[mainBondId][4];
        c = bonds[sideBondId][4];
    } else if (bonds[mainBondId][4] == bonds[sideBondId][4]) {
        a = bonds[mainBondId][3];
        b = bonds[mainBondId][4];
        c = bonds[sideBondId][3];
    }
    return [a, b, c];
}
function drawDoubleBond(bondId) {
    var secondBond;
    var sideBond = bonds.find(function (bond) {
        return searchSideBond(bondId, bond[0]);
    });
    if (sideBond == void 0) {
        secondBond = doubleSide(bonds[bondId][3], bonds[bondId][4]);
        drawBond(secondBond[0], secondBond[1], secondBond[2], secondBond[3]);
    } else {
        var abc = lineUpABC(bondId, sideBond[0]);
        secondBond = doubleSide(abc[0], abc[1], abc[2]);
        drawBond(secondBond[0], secondBond[1], secondBond[2], secondBond[3]);
    }
}
function drawTripleBond(bondId) {
    var a = bonds[bondId][3];
    var b = bonds[bondId][4];
    var baAngle = getAngle(atoms[b][1], atoms[b][2], atoms[a][1], ay = atoms[a][2]);
    var bx, by, ax, ay;
    bx = atoms[b][1] + len / 5 * Math.sin(baAngle + 3 * Math.PI / 4);
    by = atoms[b][2] - len / 5 * Math.cos(baAngle + 3 * Math.PI / 4);
    ax = atoms[a][1] + len / 5 * Math.sin(baAngle + Math.PI / 4);
    ay = atoms[a][2] - len / 5 * Math.cos(baAngle + Math.PI / 4);
    drawBond(ax, ay, bx, by);
    bx = atoms[b][1] + len / 5 * Math.sin(baAngle - 3 * Math.PI / 4);
    by = atoms[b][2] - len / 5 * Math.cos(baAngle - 3 * Math.PI / 4);
    ax = atoms[a][1] + len / 5 * Math.sin(baAngle - Math.PI / 4);
    ay = atoms[a][2] - len / 5 * Math.cos(baAngle - Math.PI / 4);
    drawBond(ax, ay, bx, by);
}
function listUpSideBond(a) {
    var bondList = [];
    for (var i = 0, l = bonds.length; i < l; i++) {
        if (bonds[i][3] == a) {
            bondList.push(i);
        } else if (bonds[i][4] == a) {
            bondList.push(i);
        }
    }
    return bondList;
}
function refreshId(listType) { //listType 0:atoms 1:bonds
    var changedAtom = [];
    if (listType == 0) {
        for (var i = 0, l = atoms.length; i < l; i++) {
            if (atoms[i][0] != i) {
                changedAtom.push([atoms[i][0],i]);
                atoms[i][0] = i;
            }
        }
        for (var k = 0, m = bonds.length; k < m; k++) {
            for(var o = 0,p = changedAtom.length; o < p; o++){
                if(changedAtom[o][0]==bonds[k][3]){
                    bonds[k][3] = changedAtom[o][1];
                }else if(changedAtom[o][0]==bonds[k][4]){
                    bonds[k][4] = changedAtom[o][1];
                }
            }
        }
    } else if (listType == 1) {
        for (var j = 0, n = bonds.length; j < n; j++) {
            if (bonds[j][0] != j) {
                bonds[j][0] = j;
            }
        }
    }
}
function redraw() {
    clear(main);
    for (var i = 0, l = bonds.length; i < l; i++) {
        drawBond(atoms[bonds[i][3]][1], atoms[bonds[i][3]][2], atoms[bonds[i][4]][1], atoms[bonds[i][4]][2]);
        switch (bonds[i][5]) {
            case 1:
                break;
            case 2:
                drawDoubleBond(i);
                break;
            case 3:
                drawTripleBond(i);
                break;
        }
    }
    for(var j = 0, la = atoms.length; j < la; j++){
        if(atoms[j][3]!="C"){
            atomSym = atoms[j][3];
            setAtom(atoms[j][1],atoms[j][2]);
        }else{
            var sideBond = listUpSideBond(j);
            if(sideBond.length==0){
                atomSym = "C";
                setAtom(atoms[j][1],atoms[j][2]);
            }
        }
    }
}
function showAtomList(){
    eff2.fillStyle="rgb(100,100,100)";
    eff2.fillRect(100,100,390,270);
    eff2.strokeStyle="rgb(0,0,0)";
    eff2.lineWidth=2;
    eff2.beginPath();
    eff2.moveTo(100,100);
    eff2.lineTo(490,100);
    eff2.lineTo(490,370);
    eff2.lineTo(100,370);
    eff2.lineTo(100,100);
    eff2.stroke();
    eff2.fillStyle="rgb(255,255,255)";
    var x,y,i,j;
    for(j=0;j<4;j++){
        y = j*60+120;
        for(i = 0;i<6;i++){
            x = i*60+120;
            eff2.fillRect(x,y,50,50);
        }
    }
    eff2.font="40px 'sunselif'";
    eff2.fillStyle="rgb(0,0,0)";
    //以下拡張予定
    y=120+41;
    for(i=0,l=symbolList1.length;i<l;i++){
        x=i*60+131;
        eff2.fillText(symbolList1[i],x,y);
    }
    //以上拡張予定
}
function inAtomList(x,y){
    var symbol;
    //以下拡張予定
    for(i=0,l=symbolList1.length;i<l;i++){
        if(120+60*i<=x&&x<=170+60*i&&120<=y&&y<=170){
            symbol = symbolList1[i];
        }
    }
    //以上拡張予定
    return symbol;
}
function setAtom(x,y){
    main.beginPath();
    main.fillStyle = "rgb(255,255,255)";
    main.arc(x,y, 10, 0, Math.PI * 2, true);
    main.fill();
    main.font="20px 'sunselif'";
    main.fillStyle="rgb(0,0,0)";
    main.fillText(atomSym,x-8,y+8);
}
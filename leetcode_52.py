# 52. N-Queens II
class Solution:
    def totalNQueens(self, n: int) -> List[List[str]]:
        res=[];nq=[['.']*n for i in range(n)];qx=[];qy=[]
        def check(i,j,qx,qy,n):
            if(i>=n or j>=n):return False
            if(i in qx):return False
            if(j in qy):return False
            for k in range(len(qx)):
                if(i+j==qx[k]+qy[k] or i-j==qx[k]-qy[k]):return False
            return True
        def nqueens(row,nq,n,qx,qy):
            if(row==n):
                res.append(deepcopy(nq))
                return
            for col in range(n):
                if(check(row,col,qx,qy,n)):
                    qx+=[row];qy+=[col];nq[row][col]='Q'
                    nqueens(row+1,nq,n,qx,qy)
                    nq[row][col]='.';qx.pop();qy.pop()
            return
        nqueens(0,nq,n,qx,qy)
        return len(res)
            

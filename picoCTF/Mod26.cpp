#include<bits/stdc++.h>
#define int long long
#define speed ios_base::sync_with_stdio(0); cin.tie(0);

#define fi first
#define se second
#define taskname ""
using namespace std;
const int maxn=1e5+10;
const int mod=998244353 ;
 
signed main()
{
    if(ifstream(taskname".inp")) 
    {
        freopen(taskname".inp", "r", stdin);
        freopen(taskname".out", "w", stdout);
    }
    speed
    string s;
    cin>>s;
    vector<char> res;
    for(int i=0; i < s.size(); i++){
        if(s[i] <= 'z' && s[i] >= 'a') {
            char c = (char)(((int)s[i]- 97 + 13)%26 + 97);
            res.push_back(c);
        }
        else if(s[i] <= 'Z' && s[i] >= 'A') {
            char c = (char)(((int)s[i] - 65 + 13)%26 + 65);
            res.push_back(c);
        }
        else res.push_back(s[i]);
    }
    for(int i =0; i < res.size(); i++){
        cout<<res[i];
    }
    return 0;
}
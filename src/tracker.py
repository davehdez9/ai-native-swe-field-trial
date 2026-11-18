import json
from pathlib import Path
class TaskStore:
    def __init__(self,path): self.path=Path(path)
    def load(self):
        if not self.path.exists(): return []
        data=json.loads(self.path.read_text())
        if not isinstance(data,list): raise ValueError('invalid tasks file')
        return data
    def save(self,rows):
        self.path.parent.mkdir(parents=True,exist_ok=True)
        temp=self.path.with_suffix(self.path.suffix+'.tmp')
        temp.write_text(json.dumps(rows,sort_keys=True))
        temp.replace(self.path)
    def add(self,identifier,title):
        if not isinstance(identifier,str) or not identifier.strip() or not isinstance(title,str) or not title.strip(): raise ValueError('required text')
        rows=self.load()
        if any(row['id']==identifier for row in rows): raise ValueError('duplicate id')
        rows.append({'id':identifier,'title':title,'done':False}); self.save(rows); return rows[-1]
    def complete(self,identifier):
        rows=self.load()
        matched=False
        for row in rows:
            if row['id']==identifier: row['done']=True;matched=True
        if not matched: raise KeyError(identifier)
        self.save(rows)

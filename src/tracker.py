"""Local single-process task store. No concurrency or production durability guarantees."""
import json
import re
from datetime import date
from pathlib import Path

_ISO = re.compile(r"\d{4}-\d{2}-\d{2}\Z", re.ASCII)

def valid_date(value):
    if not isinstance(value, str):
        raise TypeError('date must be a string in YYYY-MM-DD')
    if not _ISO.fullmatch(value):
        raise ValueError('date must be in YYYY-MM-DD')
    try: date.fromisoformat(value)
    except ValueError as exc: raise ValueError('invalid calendar date') from exc
    return value

class TaskStore:
    def __init__(self,path): self.path=Path(path)
    def load(self):
        if not self.path.exists(): return []
        data=json.loads(self.path.read_text(encoding='utf-8'))
        if not isinstance(data,list): raise ValueError('invalid tasks file')
        identifiers=set()
        for row in data:
            if not isinstance(row,dict) or not isinstance(row.get('id'),str) or not row['id'].strip() or not isinstance(row.get('title'),str) or not row['title'].strip() or type(row.get('done')) is not bool:
                raise ValueError('invalid task record')
            if row['id'] in identifiers: raise ValueError('duplicate task ID in file')
            identifiers.add(row['id'])
            if row.get('due_date') is not None: valid_date(row['due_date'])
        return data
    def save(self,rows):
        self.path.parent.mkdir(parents=True,exist_ok=True)
        temp=self.path.with_suffix(self.path.suffix+'.tmp')
        temp.write_text(json.dumps(rows,sort_keys=True),encoding='utf-8')
        temp.replace(self.path)
    def add(self,identifier,title,due_date=None):
        if not isinstance(identifier,str) or not identifier.strip() or not isinstance(title,str) or not title.strip(): raise ValueError('required text')
        if due_date is not None: valid_date(due_date)
        rows=self.load()
        if any(row['id']==identifier for row in rows): raise ValueError('duplicate id')
        item={'id':identifier,'title':title,'done':False}
        if due_date is not None: item['due_date']=due_date
        rows.append(item); self.save(rows); return item
    def complete(self,identifier):
        rows=self.load()
        matched=False
        for row in rows:
            if row['id']==identifier: row['done']=True; matched=True
        if not matched: raise KeyError(identifier)
        self.save(rows)
    def overdue(self,as_of):
        valid_date(as_of)
        return sorted((row for row in self.load() if not row['done'] and row.get('due_date') is not None and row['due_date'] < as_of),key=lambda r:(r['due_date'],r['id']))
    def search(self,query):
        """Read-only, literal, case-insensitive (casefold) title substring search in stored order."""
        if not isinstance(query,str): raise TypeError('query must be a string')
        if not query.strip(): raise ValueError('query must not be empty')
        needle=query.casefold()
        return [row for row in self.load() if needle in row['title'].casefold()]

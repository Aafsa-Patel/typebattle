import { useEffect, useMemo, useRef, useState } from 'react';
import { Check, RotateCcw, Timer, Flame, Target, ChevronRight, LockKeyhole } from 'lucide-react';
import { api, getUser } from '../services/api';
import './Practice.css';

const LEVELS=[
 {id:'letters',title:'Warm-up Letters',tag:'EASIEST',time:45,text:'asdf jkl; asdf jkl; fjfj dkdk slsl'},
 {id:'words',title:'Simple Words',tag:'EASY',time:45,text:'ask add fall dad sad lad all ask fall'},
 {id:'sentences',title:'Short Sentences',tag:'STARTER',time:60,text:'small steps build strong typing habits.'},
 {id:'keyboard',title:'Full Keyboard',tag:'CHALLENGE',time:60,text:'quick brown fox jumps over lazy dogs.'},
];
const rows=[['q','w','e','r','t','y','u','i','o','p'],['a','s','d','f','g','h','j','k','l'],['z','x','c','v','b','n','m']];
export default function Practice(){
 const [levelIndex,setLevelIndex]=useState(0),[input,setInput]=useState(''),[started,setStarted]=useState(false),[finished,setFinished]=useState(false),[time,setTime]=useState(LEVELS[0].time),[message,setMessage]=useState(''),[saving,setSaving]=useState(false); const ref=useRef(null); const saved=useRef(false); const level=LEVELS[levelIndex];
 const correct=useMemo(()=>input.split('').reduce((n,c,i)=>n+(c===level.text[i]?1:0),0),[input,level]); const errors=Math.max(0,input.length-correct); const elapsed=Math.max(1,level.time-time); const wpm=Math.max(0,Math.round(correct/5/(elapsed/60))); const accuracy=input.length?Math.round(correct/input.length*100):100; const current=level.text[input.length]||'';
 const reset=()=>{setInput('');setStarted(false);setFinished(false);setTime(level.time);setMessage('');saved.current=false;setTimeout(()=>ref.current?.focus(),0)};
 const choose=(i)=>{setLevelIndex(i);const l=LEVELS[i];setInput('');setStarted(false);setFinished(false);setTime(l.time);setMessage('');saved.current=false;setTimeout(()=>ref.current?.focus(),0)};
 useEffect(()=>{if(!started||finished)return; if(time<=0){setFinished(true);return;} const id=setInterval(()=>setTime(t=>t-1),1000);return()=>clearInterval(id)},[started,finished,time]);
 useEffect(()=>{if(!started||finished||!input)return; if(input.length>=level.text.length)setFinished(true)},[input,level.text.length,started,finished]);
 useEffect(()=>{if(!finished||saved.current)return; saved.current=true; const user=getUser(); if(!user){setMessage('Practice complete. Sign in to save this run.');return;} setSaving(true);api.savePractice({passage:level.text,wpm,accuracy,errors,time_taken:elapsed}).then(()=>setMessage('Result saved to your profile.')).catch(e=>{saved.current=false;setMessage(e.message)}).finally(()=>setSaving(false))},[finished]);
 const onChange=e=>{let value=e.target.value;if(!started){setStarted(true);setMessage('')}if(value.length>level.text.length)value=value.slice(0,level.text.length);setInput(value)};
 return <main className="page practice-page"><div className="practice-head"><div><div className="eyebrow">Practice Lab</div><h1 className="section-title">Start easy. Build accuracy. Then go fast.</h1><p>Each level is designed to feel comfortable before the next one unlocks.</p></div><div className="streak"><Flame size={18}/><strong>Accuracy first</strong><span>Speed follows.</span></div></div>
 <div className="level-strip">{LEVELS.map((l,i)=><button key={l.id} className={`level-card ${i===levelIndex?'selected':''} ${i>levelIndex?'locked':''}`} onClick={()=>i<=levelIndex&&choose(i)}><span>{i>levelIndex?<LockKeyhole size={15}/>:<span className="level-num">{i+1}</span>}</span><div><b>{l.title}</b><small>{l.tag}</small></div>{i===levelIndex&&<ChevronRight size={17}/>}</button>)}</div>
 <section className="practice-shell glass"><div className="stats"><Stat icon={<Timer/>} label="Time" value={`${time}s`}/><Stat icon={<Target/>} label="WPM" value={wpm}/><Stat icon={<Check/>} label="Accuracy" value={`${accuracy}%`}/><Stat icon={<Flame/>} label="Errors" value={errors}/></div>
 <div className="progress"><i style={{width:`${Math.min(100,input.length/level.text.length*100)}%`}}/></div>
 <div className="prompt">{level.text.split('').map((c,i)=><span key={i} className={i<input.length?(input[i]===c?'correct':'wrong'):i===input.length?'current':''}>{c===' '?'·':c}</span>)}</div>
 <textarea ref={ref} autoFocus value={input} onChange={onChange} disabled={finished} spellCheck="false" aria-label="Type the text shown above" placeholder="Click here and start typing…" />
 <div className="practice-bottom"><div><b>{finished?'Run complete':'Ready when you are'}</b><span>{saving?'Saving…':message||`Level ${levelIndex+1} of ${LEVELS.length} · ${level.title}`}</span></div><div className="actions"><button className="btn" onClick={reset}><RotateCcw size={17}/> Restart</button>{finished&&levelIndex<LEVELS.length-1&&<button className="btn btn-primary" onClick={()=>choose(levelIndex+1)}>Next level <ChevronRight size={17}/></button>}</div></div>
 <div className="keyboard">{rows.map(row=>row.map(k=><span key={k} className={k===current.toLowerCase()?'hot':''}>{k}</span>))}<span className={current===' '?'hot':''} style={{gridColumn:'2 / span 9'}}>space</span></div>
 </section></main>}
function Stat({icon,label,value}){return <div className="stat"><span>{icon}</span><small>{label}</small><strong>{value}</strong></div>}

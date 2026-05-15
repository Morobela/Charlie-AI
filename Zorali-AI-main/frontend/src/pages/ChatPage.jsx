import { useEffect, useState } from 'react'
import { useProjectStore } from '../store/projectStore'
import { useChatStore } from '../store/chatStore'

export default function ChatPage(){
  const { projects, selectedProjectId, loadProjects, selectProject } = useProjectStore()
  const { messages, loadHistory } = useChatStore()
  const [text, setText] = useState('')

  useEffect(() => { loadProjects() }, [loadProjects])
  useEffect(() => { loadHistory(selectedProjectId) }, [selectedProjectId, loadHistory])

  return <div style={{padding:16}}>
    <h2>Chat</h2>
    <select value={selectedProjectId || ''} onChange={(e)=>selectProject(e.target.value)}>
      <option value="">Select project</option>
      {projects.map(p => <option key={p.id} value={p.id}>{p.name}</option>)}
    </select>
    <div>{messages.map(m => <div key={m.id}><b>{m.role}:</b> {m.content}</div>)}</div>
    <input value={text} onChange={(e)=>setText(e.target.value)} placeholder='Use websocket chat to send messages'/>
  </div>
}

import { useState, useRef, useEffect } from 'react'
import { Button } from '@/components/ui/button.jsx'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card.jsx'
import { Input } from '@/components/ui/input.jsx'
import { Badge } from '@/components/ui/badge.jsx'
import { Textarea } from '@/components/ui/textarea.jsx'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs.jsx'
import { 
  MessageCircle, 
  Sparkles, 
  Calendar, 
  DollarSign, 
  Lightbulb, 
  Image, 
  Send, 
  Bot,
  User,
  Mic,
  MicOff,
  Settings,
  Zap,
  TrendingUp,
  Clock,
  CheckCircle
} from 'lucide-react'
import './App.css'

function App() {
  const [messages, setMessages] = useState([
    {
      id: 1,
      type: 'bot',
      content: 'Olá! Sou o Qognix Genius, seu assistente de IA criativo. Como posso ajudá-lo hoje?',
      timestamp: new Date()
    }
  ])
  const [inputMessage, setInputMessage] = useState('')
  const [isListening, setIsListening] = useState(false)
  const [activeTab, setActiveTab] = useState('chat')
  const messagesEndRef = useRef(null)

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" })
  }

  useEffect(() => {
    scrollToBottom()
  }, [messages])

  const handleSendMessage = () => {
    if (inputMessage.trim()) {
      const newMessage = {
        id: messages.length + 1,
        type: 'user',
        content: inputMessage,
        timestamp: new Date()
      }
      
      setMessages([...messages, newMessage])
      setInputMessage('')
      
      // Simular resposta do bot
      setTimeout(() => {
        const botResponse = {
          id: messages.length + 2,
          type: 'bot',
          content: generateBotResponse(inputMessage),
          timestamp: new Date()
        }
        setMessages(prev => [...prev, botResponse])
      }, 1000)
    }
  }

  const generateBotResponse = (userMessage) => {
    const message = userMessage.toLowerCase()
    
    if (message.includes('post') || message.includes('instagram') || message.includes('facebook')) {
      return '📱 Vou criar um post criativo para você! Aqui está uma sugestão:\n\n"🌟 Transforme seu dia com pequenas ações! ✨\n\nCada momento é uma oportunidade de crescer e brilhar. 💪\n\n#motivacao #crescimento #sucesso #mindset #inspiracao #vida"'
    }
    
    if (message.includes('agenda') || message.includes('compromisso')) {
      return '📅 Analisando sua agenda... Sugiro bloquear 2 horas amanhã das 9h às 11h para foco profundo em projetos importantes. Também recomendo uma pausa de 15 minutos a cada 2 horas para manter a produtividade!'
    }
    
    if (message.includes('ideia') || message.includes('criativo')) {
      return '💡 Aqui estão algumas ideias criativas:\n\n• Campanha "Segundas Motivacionais" com dicas semanais\n• Série de vídeos curtos sobre produtividade\n• Challenge de 30 dias para formar novos hábitos\n• Podcast sobre histórias de sucesso\n• Workshop online interativo'
    }
    
    if (message.includes('financ') || message.includes('dinheiro') || message.includes('gasto')) {
      return '💰 Com base nos seus padrões de gastos, sugiro:\n\n• Criar uma reserva de emergência de R$ 500/mês\n• Revisar assinaturas não utilizadas (economia potencial: R$ 150/mês)\n• Investir 20% da renda em fundos de baixo risco\n• Usar a regra 50-30-20 para organizar o orçamento'
    }
    
    return '✨ Entendi! Estou processando sua solicitação e vou te ajudar da melhor forma possível. Posso criar conteúdo, organizar sua agenda, sugerir ideias criativas ou ajudar com análises financeiras. O que você gostaria de explorar primeiro?'
  }

  const toggleListening = () => {
    setIsListening(!isListening)
    // Aqui seria implementada a funcionalidade de reconhecimento de voz
  }

  const quickActions = [
    { icon: Sparkles, label: 'Criar Post', action: () => setInputMessage('Crie um post criativo para Instagram') },
    { icon: Calendar, label: 'Otimizar Agenda', action: () => setInputMessage('Analise minha agenda e sugira melhorias') },
    { icon: Lightbulb, label: 'Gerar Ideias', action: () => setInputMessage('Preciso de ideias criativas para meu projeto') },
    { icon: DollarSign, label: 'Análise Financeira', action: () => setInputMessage('Analise meus gastos e dê sugestões') }
  ]

  const features = [
    {
      icon: MessageCircle,
      title: 'Chat Inteligente',
      description: 'Conversas naturais com IA avançada que entende contexto e nuances.'
    },
    {
      icon: Sparkles,
      title: 'Geração Criativa',
      description: 'Crie posts, textos, ideias e conteúdo original em segundos.'
    },
    {
      icon: TrendingUp,
      title: 'Análise Proativa',
      description: 'Insights automáticos sobre produtividade, finanças e otimizações.'
    },
    {
      icon: Zap,
      title: 'Automação Inteligente',
      description: 'Execute múltiplas tarefas simultaneamente com eficiência máxima.'
    }
  ]

  const stats = [
    { label: 'Tarefas Automatizadas', value: '1,247', icon: CheckCircle },
    { label: 'Tempo Economizado', value: '156h', icon: Clock },
    { label: 'Posts Criados', value: '89', icon: Image },
    { label: 'Insights Gerados', value: '342', icon: TrendingUp }
  ]

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-purple-50">
      <div className="container mx-auto px-4 py-8">
        {/* Header */}
        <div className="text-center mb-8">
          <div className="flex items-center justify-center gap-3 mb-4">
            <div className="p-3 bg-gradient-to-r from-blue-600 to-purple-600 rounded-full">
              <Bot className="w-8 h-8 text-white" />
            </div>
            <h1 className="text-4xl font-bold bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">
              Qognix Genius
            </h1>
          </div>
          <p className="text-xl text-gray-600 max-w-2xl mx-auto">
            Seu assistente de IA criativo que vai além da automação - oferece insights proativos, 
            gera conteúdo original e otimiza sua produtividade de forma inteligente.
          </p>
        </div>

        <Tabs value={activeTab} onValueChange={setActiveTab} className="w-full">
          <TabsList className="grid w-full grid-cols-4 mb-8">
            <TabsTrigger value="chat">Chat</TabsTrigger>
            <TabsTrigger value="features">Funcionalidades</TabsTrigger>
            <TabsTrigger value="stats">Estatísticas</TabsTrigger>
            <TabsTrigger value="settings">Configurações</TabsTrigger>
          </TabsList>

          <TabsContent value="chat" className="space-y-6">
            {/* Quick Actions */}
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <Zap className="w-5 h-5" />
                  Ações Rápidas
                </CardTitle>
                <CardDescription>
                  Clique em uma das opções abaixo para começar rapidamente
                </CardDescription>
              </CardHeader>
              <CardContent>
                <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                  {quickActions.map((action, index) => (
                    <Button
                      key={index}
                      variant="outline"
                      className="h-20 flex flex-col gap-2 hover:bg-gradient-to-r hover:from-blue-50 hover:to-purple-50"
                      onClick={action.action}
                    >
                      <action.icon className="w-6 h-6" />
                      <span className="text-sm">{action.label}</span>
                    </Button>
                  ))}
                </div>
              </CardContent>
            </Card>

            {/* Chat Interface */}
            <Card className="h-96">
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <MessageCircle className="w-5 h-5" />
                  Conversa
                </CardTitle>
              </CardHeader>
              <CardContent className="flex flex-col h-full">
                <div className="flex-1 overflow-y-auto space-y-4 mb-4">
                  {messages.map((message) => (
                    <div
                      key={message.id}
                      className={`flex gap-3 ${message.type === 'user' ? 'justify-end' : 'justify-start'}`}
                    >
                      <div className={`flex gap-3 max-w-[80%] ${message.type === 'user' ? 'flex-row-reverse' : 'flex-row'}`}>
                        <div className={`p-2 rounded-full ${message.type === 'user' ? 'bg-blue-600' : 'bg-purple-600'}`}>
                          {message.type === 'user' ? (
                            <User className="w-4 h-4 text-white" />
                          ) : (
                            <Bot className="w-4 h-4 text-white" />
                          )}
                        </div>
                        <div className={`p-3 rounded-lg ${
                          message.type === 'user' 
                            ? 'bg-blue-600 text-white' 
                            : 'bg-gray-100 text-gray-800'
                        }`}>
                          <p className="whitespace-pre-wrap">{message.content}</p>
                          <span className="text-xs opacity-70 mt-1 block">
                            {message.timestamp.toLocaleTimeString()}
                          </span>
                        </div>
                      </div>
                    </div>
                  ))}
                  <div ref={messagesEndRef} />
                </div>
                
                <div className="flex gap-2">
                  <Input
                    value={inputMessage}
                    onChange={(e) => setInputMessage(e.target.value)}
                    placeholder="Digite sua mensagem..."
                    onKeyPress={(e) => e.key === 'Enter' && handleSendMessage()}
                    className="flex-1"
                  />
                  <Button
                    onClick={toggleListening}
                    variant={isListening ? "default" : "outline"}
                    size="icon"
                  >
                    {isListening ? <MicOff className="w-4 h-4" /> : <Mic className="w-4 h-4" />}
                  </Button>
                  <Button onClick={handleSendMessage} size="icon">
                    <Send className="w-4 h-4" />
                  </Button>
                </div>
              </CardContent>
            </Card>
          </TabsContent>

          <TabsContent value="features" className="space-y-6">
            <div className="grid md:grid-cols-2 gap-6">
              {features.map((feature, index) => (
                <Card key={index} className="hover:shadow-lg transition-shadow">
                  <CardHeader>
                    <CardTitle className="flex items-center gap-3">
                      <div className="p-2 bg-gradient-to-r from-blue-600 to-purple-600 rounded-lg">
                        <feature.icon className="w-6 h-6 text-white" />
                      </div>
                      {feature.title}
                    </CardTitle>
                    <CardDescription>{feature.description}</CardDescription>
                  </CardHeader>
                  <CardContent>
                    <Button variant="outline" className="w-full">
                      Explorar Funcionalidade
                    </Button>
                  </CardContent>
                </Card>
              ))}
            </div>
          </TabsContent>

          <TabsContent value="stats" className="space-y-6">
            <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-6">
              {stats.map((stat, index) => (
                <Card key={index}>
                  <CardContent className="p-6">
                    <div className="flex items-center justify-between">
                      <div>
                        <p className="text-sm font-medium text-gray-600">{stat.label}</p>
                        <p className="text-3xl font-bold text-gray-900">{stat.value}</p>
                      </div>
                      <stat.icon className="w-8 h-8 text-blue-600" />
                    </div>
                  </CardContent>
                </Card>
              ))}
            </div>
            
            <Card>
              <CardHeader>
                <CardTitle>Resumo de Atividades</CardTitle>
                <CardDescription>Suas interações com o assistente nos últimos 30 dias</CardDescription>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  <div className="flex items-center justify-between">
                    <span>Posts Criativos Gerados</span>
                    <Badge variant="secondary">89 posts</Badge>
                  </div>
                  <div className="flex items-center justify-between">
                    <span>Análises Financeiras</span>
                    <Badge variant="secondary">23 relatórios</Badge>
                  </div>
                  <div className="flex items-center justify-between">
                    <span>Otimizações de Agenda</span>
                    <Badge variant="secondary">156 sugestões</Badge>
                  </div>
                  <div className="flex items-center justify-between">
                    <span>Ideias Criativas</span>
                    <Badge variant="secondary">342 conceitos</Badge>
                  </div>
                </div>
              </CardContent>
            </Card>
          </TabsContent>

          <TabsContent value="settings" className="space-y-6">
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <Settings className="w-5 h-5" />
                  Configurações do Assistente
                </CardTitle>
                <CardDescription>
                  Personalize a experiência do seu assistente de IA
                </CardDescription>
              </CardHeader>
              <CardContent className="space-y-6">
                <div>
                  <label className="text-sm font-medium">Modo de Operação</label>
                  <div className="grid grid-cols-3 gap-2 mt-2">
                    <Button variant="outline" size="sm">Foco Total</Button>
                    <Button variant="default" size="sm">Criativo</Button>
                    <Button variant="outline" size="sm">Relax</Button>
                  </div>
                </div>
                
                <div>
                  <label className="text-sm font-medium">Tom de Voz</label>
                  <div className="grid grid-cols-2 gap-2 mt-2">
                    <Button variant="outline" size="sm">Profissional</Button>
                    <Button variant="default" size="sm">Amigável</Button>
                  </div>
                </div>
                
                <div>
                  <label className="text-sm font-medium">Notificações Proativas</label>
                  <div className="flex items-center space-x-2 mt-2">
                    <input type="checkbox" defaultChecked />
                    <span className="text-sm">Receber sugestões automáticas</span>
                  </div>
                </div>
                
                <div>
                  <label className="text-sm font-medium">Integração WhatsApp</label>
                  <div className="mt-2">
                    <Input placeholder="Número do WhatsApp" />
                    <Button className="mt-2 w-full">Conectar WhatsApp</Button>
                  </div>
                </div>
              </CardContent>
            </Card>
          </TabsContent>
        </Tabs>
      </div>
    </div>
  )
}

export default App


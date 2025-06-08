import express from 'express'
import dotenv from 'dotenv'
import mongoose from 'mongoose'
import bcrypt from 'bcrypt'
import jwt from 'jsonwebtoken'

dotenv.config()

const jwtSecret = process.env.JWT_SECRET
if (!jwtSecret) {
    throw new Error('JWT_SECRET is not defined in .env file')
}

const mongoURI = process.env.MONGO_URI
if (!mongoURI) {
    throw new Error('MONGO_URI is not defined in .env file')
}

await mongoose.connect(mongoURI)
const alertSchema = new mongoose.Schema({
    'class': String,
    'timestamp': Date,
    'record': String,
    'thumb': String,
})
const Alert = mongoose.model('Alert', alertSchema, 'alerts')

const userSchema = new mongoose.Schema({
    'email': String,
    'password': String
})
const User = mongoose.model('User', userSchema, 'users')

function validateToken(req, res, next) {
    let token = req.headers['authorization']

    if (token === null || token === undefined) return res.sendStatus(401)
    if (!token.startsWith('Bearer ')) return res.sendStatus(401)
    token = token.replace('Bearer ', '')

    try {
        const tokenBody = jwt.verify(token, jwtSecret)
        req.tokenBody = tokenBody
        next()
    } catch (error) {
        return res.sendStatus(401)
    }
}

const app = express()
app.use(express.json())

app.use(express.static('public'))
app.use('/recordings', validateToken, express.static('../recordings'))

app.get('/alerts', validateToken, async (req, res) => {
    const { page, size } = req.query
    const pageNumber = parseInt(page ?? 1) || 1
    const pageSize = parseInt(size ?? 10) || 10

    const alerts = await Alert.find()
        .skip((pageNumber - 1) * pageSize)
        .limit(pageSize)
        .sort({ timestamp: -1 })
    const total = await Alert.countDocuments()
    const totalPages = Math.ceil(total / pageSize)
    res.json({
        alerts,
        total,
        page: pageNumber,
        totalPages,
        hasNext: pageNumber < totalPages,
        hasPrev: pageNumber > 1,
    })
})

app.get('/quick-stats', validateToken, async (req, res) => {
    // get amount by class of today
    const today = new Date()
    today.setHours(0, 0, 0, 0)
    const tomorrow = new Date(today)
    tomorrow.setDate(today.getDate() + 1)
    const stats = await Alert.aggregate([
        {
            $match: {
                timestamp: {
                    $gte: today,
                    $lt: tomorrow,
                },
            },
        },
        {
            $group: {
                _id: '$class',
                count: { $sum: 1 },
            },
        },
    ])
    const total = stats.reduce((acc, s) => acc + s.count, 0)

    const statsMap = new Map()
    stats.forEach(s => {
        statsMap.set(s._id, s.count)
    })
    const statsObj = {
        total,
        classes: {},
    }
    statsMap.forEach((count, cls) => {
        statsObj.classes[cls] = count
    })
    res.json(statsObj)
})

// 1) Série diária (últimos 30 dias)
app.get('/stats/daily', validateToken, async (_, res) => {
    const today = new Date(); today.setHours(0, 0, 0, 0);
    const past = new Date(today); past.setDate(past.getDate() - 29);
    const data = await Alert.aggregate([
        { $match: { timestamp: { $gte: past, $lt: new Date(today.getTime() + 24 * 60 * 60 * 1000) } } },
        {
            $group: {
                _id: { $dateToString: { date: '$timestamp', format: '%Y-%m-%d' } },
                count: { $sum: 1 }
            }
        },
        { $sort: { '_id': 1 } }
    ]);
    // preenche datas faltantes com zero
    const labels = [], series = [];
    for (let d = new Date(past); d <= today; d.setDate(d.getDate() + 1)) {
        const key = d.toISOString().substring(0, 10);
        labels.push(key);
        const item = data.find(x => x._id === key);
        series.push(item ? item.count : 0);
    }
    res.json({ labels, series });
});

// 2) Totais por classe (últimos 30 dias)
app.get('/stats/classes', validateToken, async (_, res) => {
    const since = new Date(); since.setDate(since.getDate() - 30);
    const data = await Alert.aggregate([
        { $match: { timestamp: { $gte: since } } },
        { $group: { _id: '$class', count: { $sum: 1 } } },
        { $sort: { count: -1 } }
    ]);
    const labels = data.map(x => x._id);
    const series = data.map(x => x.count);
    res.json({ labels, series });
});

// 3) Distribuição horária (0–23h, últimos 7 dias)
app.get('/stats/hourly', validateToken, async (_, res) => {
    const since = new Date(); since.setDate(since.getDate() - 7);
    const data = await Alert.aggregate([
        { $match: { timestamp: { $gte: since } } },
        {
            $group: {
                _id: { $hour: '$timestamp' },
                count: { $sum: 1 }
            }
        },
        { $sort: { '_id': 1 } }
    ]);
    // preenche 0–23
    const labels = Array.from({ length: 24 }, (_, i) => i.toString());
    const series = labels.map(h => {
        const it = data.find(x => x._id === parseInt(h));
        return it ? it.count : 0;
    });
    res.json({ labels, series });
});

// 4) Heatmap dia × classe (últimos 30 dias)
app.get('/stats/heatmap', validateToken, async (_, res) => {
    const today = new Date(); today.setHours(0, 0, 0, 0);
    const past = new Date(today); past.setDate(past.getDate() - 29);
    const data = await Alert.aggregate([
        { $match: { timestamp: { $gte: past, $lt: new Date(today.getTime() + 86400000) } } },
        {
            $group: {
                _id: {
                    day: { $dateToString: { date: '$timestamp', format: '%Y-%m-%d' } },
                    cls: '$class'
                },
                count: { $sum: 1 }
            }
        },
        { $sort: { '_id.day': 1 } }
    ]);
    // coleciona labels dias e classes
    const days = [], classes = Array.from(new Set(data.map(x => x._id.cls)));
    for (let d = new Date(past); d <= today; d.setDate(d.getDate() + 1)) {
        days.push(d.toISOString().substring(0, 10));
    }
    // montar matriz [classes.length][days.length]
    const matrix = classes.map(cls =>
        days.map(day => {
            const it = data.find(x => x._id.day === day && x._id.cls === cls);
            return it ? it.count : 0;
        })
    );
    res.json({ days, classes, matrix });
});

app.post('/users', validateToken, async (req, res) => {
    const { email, password } = req.body

    const user = new User({
        email,
        password: await bcrypt.hash(password, 10)
    })

    await user.save()
    res.sendStatus(204)
})

app.post('/token', async (req, res) => {
    const { email, password } = req.body

    const savedUser = await User.where({ email }).findOne()
    if (savedUser === null) return res.sendStatus(401)

    if (!await bcrypt.compare(password, savedUser.password)) return res.sendStatus(401)

    const token = jwt.sign({ userId: savedUser.id, email: savedUser.email }, process.env.JWT_SECRET)
    res.json({ token })
})

app.listen(3000, () => {
    console.log('Server is running on http://localhost:3000')
})

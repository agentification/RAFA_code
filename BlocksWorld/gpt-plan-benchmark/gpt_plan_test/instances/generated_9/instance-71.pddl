

(define (problem BW-rand-9)
(:domain blocksworld-4ops)
(:objects a b c d e f g h i )
(:init
(handempty)
(on a c)
(on b i)
(on c e)
(ontable d)
(on e g)
(on f a)
(on g d)
(on h b)
(ontable i)
(clear f)
(clear h)
)
(:goal
(and
(on a b)
(on b c)
(on c g)
(on d a)
(on e d)
(on f i)
(on g f)
(on h e))
)
)



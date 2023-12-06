

(define (problem BW-rand-9)
(:domain blocksworld-4ops)
(:objects a b c d e f g h i )
(:init
(handempty)
(on a e)
(on b g)
(on c i)
(on d h)
(on e d)
(on f b)
(on g c)
(ontable h)
(ontable i)
(clear a)
(clear f)
)
(:goal
(and
(on b a)
(on c e)
(on d i)
(on e g)
(on h b)
(on i f))
)
)



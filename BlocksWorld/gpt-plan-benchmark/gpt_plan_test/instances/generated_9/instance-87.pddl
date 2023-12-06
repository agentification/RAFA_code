

(define (problem BW-rand-9)
(:domain blocksworld-4ops)
(:objects a b c d e f g h i )
(:init
(handempty)
(on a h)
(ontable b)
(ontable c)
(on d a)
(on e f)
(on f i)
(on g d)
(on h b)
(on i g)
(clear c)
(clear e)
)
(:goal
(and
(on a h)
(on c g)
(on e c)
(on g i)
(on h d)
(on i f))
)
)



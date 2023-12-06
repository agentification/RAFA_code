

(define (problem BW-rand-9)
(:domain blocksworld-4ops)
(:objects a b c d e f g h i )
(:init
(handempty)
(ontable a)
(on b g)
(ontable c)
(on d a)
(on e i)
(on f c)
(on g d)
(on h b)
(ontable i)
(clear e)
(clear f)
(clear h)
)
(:goal
(and
(on a g)
(on b e)
(on c d)
(on e a)
(on f i)
(on i b))
)
)



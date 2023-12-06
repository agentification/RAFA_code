

(define (problem BW-rand-9)
(:domain blocksworld-4ops)
(:objects a b c d e f g h i )
(:init
(handempty)
(on a b)
(on b g)
(on c f)
(ontable d)
(on e c)
(ontable f)
(on g i)
(on h e)
(ontable i)
(clear a)
(clear d)
(clear h)
)
(:goal
(and
(on a f)
(on b e)
(on d i)
(on e a)
(on f g)
(on h b)
(on i c))
)
)


